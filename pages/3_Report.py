"""
Reports page - View scan history and download PDF reports.
"""
import os
import streamlit as st
import pandas as pd
from utils.styles import load_css, section_header, info_message, risk_badge, metric_card
from services.database_service import DatabaseService
from services.pdf_service import PDFService
from models.risk_classifier import classify_all_risks, classify_risk
from models.recommendation_engine import RecommendationEngine


def show():
    """Display the reports page."""
    load_css()
    
    st.markdown('<div class="main-header" style="font-family:monospace; text-transform:uppercase;">[SYS] CLINICAL TELEMETRY & HISTORICAL REPORTS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header" style="font-family:monospace;">> ACCESSING SECURE OFFLINE STORAGE...</div>',
        unsafe_allow_html=True
    )
    
    db = DatabaseService()
    pdf_service = PDFService()
    
    # Get scan history
    scans = db.get_scan_history(limit=50)
    
    if not scans:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem; background-color: #0a0a0a; border: 1px solid #333;">
            <div style="font-size:2rem; font-family:monospace; color:#666;">[DATABASE EMPTY]</div>
            <p style="font-family:monospace; color:#888;">> Execute initial diagnostic inference to populate local tables.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("[>] INITIALIZE SCAN MODULE", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Eye_Scan.py")
        return
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Logs", str(len(scans)), "", "blue")
    with col2:
        high_risk_count = sum(1 for s in scans if s.get("risk_level") == "High")
        metric_card("[CRITICAL] Events", str(high_risk_count), "", "red")
    with col3:
        medium_risk = sum(1 for s in scans if s.get("risk_level") == "Medium")
        metric_card("[ELEVATED] Events", str(medium_risk), "", "orange")
    with col4:
        low_risk = sum(1 for s in scans if s.get("risk_level") == "Low")
        metric_card("[NOMINAL] Events", str(low_risk), "", "green")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scan history table
    section_header("[/] LOG ARCHIVE")
    
    # Search/filter
    search = st.text_input("🔍 Search by patient name or scan ID", "")
    
    # Filter scans
    filtered_scans = scans
    if search:
        search_lower = search.lower()
        filtered_scans = [
            s for s in scans
            if search_lower in str(s.get("patient_name", "")).lower()
            or search_lower in str(s.get("id", ""))
        ]
    
    # Display scans
    for scan in filtered_scans:
        scan_id = scan.get("id", "N/A")
        patient_name = scan.get("patient_name", "Anonymous")
        created_at = scan.get("created_at", "Unknown")
        risk_level = scan.get("risk_level", "Unknown")
        
        # Format date
        if created_at and created_at != "Unknown":
            try:
                from datetime import datetime
                dt = datetime.strptime(created_at.split(".")[0], "%Y-%m-%d %H:%M:%S")
                created_at = dt.strftime("%b %d, %Y at %I:%M %p")
            except:
                pass
        
        risk_color = {"Low": "green", "Medium": "orange", "High": "red"}.get(risk_level, "gray")
        risk_emoji = {"Low": "[NOMINAL]", "Medium": "[ELEVATED]", "High": "[CRITICAL]"}.get(risk_level, "[UNKNOWN]")
        
        st.markdown(f"""
        <div class="card" style="padding: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>Scan #{scan_id}</strong> — {patient_name}
                    <br>
                    <small style="color:#888;">{created_at}</small>
                </div>
                <div>
                    <span class="risk-{risk_color}" style="display: inline-block;">
                        {risk_emoji} {risk_level}
                    </span>
                </div>
            </div>
            <div style="margin-top: 0.5rem; font-family:monospace;">
                <small>
                    CPI (Pallor): {scan.get('anemia_score', 0)} | 
                    SIR (Icterus): {scan.get('jaundice_score', 0)} | 
                    VIS (Redness): {scan.get('redness_score', 0)} | 
                    OSI (Inflammation): {scan.get('inflammation_score', 0)}
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons for each scan
        col_a, col_b = st.columns([1, 4])
        with col_a:
            if st.button(f"[>] View Details #{scan_id}", key=f"view_{scan_id}"):
                st.session_state["selected_scan_id"] = scan_id
                st.rerun()
    
    # Selected Scan Details
    selected_scan_id = st.session_state.get("selected_scan_id")
    
    if selected_scan_id:
        st.markdown("---")
        section_header(f"[*] Scan #{selected_scan_id} Details")
        
        scan = db.get_scan_by_id(selected_scan_id)
        
        if scan:
            # Build analysis dict
            analysis = {
                "anemia_score": scan.get("anemia_score", 0),
                "jaundice_score": scan.get("jaundice_score", 0),
                "redness_score": scan.get("redness_score", 0),
                "inflammation_score": scan.get("inflammation_score", 0),
                "anemia_explanation": scan.get("anemia_explanation", ""),
                "jaundice_explanation": scan.get("jaundice_explanation", ""),
                "redness_explanation": scan.get("redness_explanation", ""),
                "inflammation_explanation": scan.get("inflammation_explanation", ""),
                "overall_health": scan.get("overall_health", "unknown"),
                "additional_findings": scan.get("additional_findings", ""),
                "urgent_care_needed": bool(scan.get("urgent_care_needed", 0)),
                "doctor_consultation_advice": scan.get("doctor_consultation_advice", "")
            }
            
            risks = classify_all_risks(analysis)
            recommender = RecommendationEngine()
            recommendations = recommender.get_all_recommendations(analysis)
            
            patient_info = {
                "name": scan.get("patient_name", "Anonymous"),
                "age": scan.get("age", 0),
                "gender": scan.get("gender", "Not specified")
            }
            
            cols = st.columns(4)
            conditions = [
                ("CPI (Pallor)", analysis.get("anemia_score", 0), risks.get("anemia", {})),
                ("SIR (Icterus)", analysis.get("jaundice_score", 0), risks.get("jaundice", {})),
                ("VIS (Redness)", analysis.get("redness_score", 0), risks.get("redness", {})),
                ("OSI (Inflamm.)", analysis.get("inflammation_score", 0), risks.get("inflammation", {}))
            ]
            
            for i, (name, score, risk) in enumerate(conditions):
                with cols[i]:
                    color = risk.get("color", "gray")
                    color_map = {"green": "#28a745", "orange": "#ff9800", "red": "#dc3545", "gray": "#6c757d"}
                    hex_color = color_map.get(color, "#6c757d")
                    
                    st.markdown(f"""
                    <div class="card" style="text-align: center; border-top: 4px solid {hex_color};">
                        <h4 style="margin:0; color:#333;">{name}</h4>
                        <div style="font-size:2rem; font-weight:700; color:{hex_color}; margin:0.3rem 0;">{int(score)}</div>
                        <span class="risk-{color}" style="display: inline-block;">{risk.get('emoji', '')} {risk.get('level', 'Unknown')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Generate PDF
            if st.button("[↓] GENERATE PDF REPORT", use_container_width=True, type="primary"):
                with st.spinner("Processing PDF Matrix..."):
                    image_path = scan.get("image_path")
                    if image_path and os.path.exists(image_path):
                        pdf_path = pdf_service.generate_report(
                            patient_info=patient_info,
                            image_path=image_path,
                            analysis=analysis,
                            recommendations=recommendations,
                            risk_classifications=risks
                        )
                        
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        
                        st.download_button(
                            label="[↓] DOWNLOAD REPORT.PDF",
                            data=pdf_bytes,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("[SYS] REPORT COMPILED SUCCESSFULLY")
                    else:
                        st.error("[ERR] SOURCE IMAGERY MISSING")
            
            if st.button("[X] CLOSE DETAILS", use_container_width=True):
                del st.session_state["selected_scan_id"]
                st.rerun()
        else:
            st.error("Scan not found.")
            if "selected_scan_id" in st.session_state:
                del st.session_state["selected_scan_id"]
    
    # Clear history button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("[!] PURGE ALL HISTORICAL LOGS", use_container_width=True, type="secondary"):
        if st.checkbox("WARNING: Irreversible deletion protocol.", key="confirm_clear"):
            # Note: For safety, we don't actually delete DB data from UI
            st.warning("[SYS] DB PURGE LOCKED FOR SECURITY.")
    
    st.markdown("""
    <div class="footer">
        All scan data is stored locally on this device.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    # Need to import os for the PDF generation check
    import os
    show()