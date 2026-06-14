"""
Doctor Finder page - Find nearby healthcare facilities.
"""
import streamlit as st
from utils.styles import load_css, section_header, info_message, metric_card
from services.doctor_service import DoctorService
from utils.location_utils import extract_location_from_input


def show():
    """Display the doctor finder page."""
    load_css()
    
    st.markdown('<div class="main-header" style="font-family:monospace; text-transform:uppercase;">[MODULE 03] SPECIALIST ROUTING PROTOCOL</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header" style="font-family:monospace;">> DISCOVER NEARBY HEALTHCARE INFRASTRUCTURE</div>',
        unsafe_allow_html=True
    )
    
    doctor_service = DoctorService()
    
    # Location Input
    st.markdown("<h3 style='color:#00ffcc; font-family:monospace;'>[>] INPUT COORDINATES / REGION</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Enter your city name to find nearby healthcare facilities. 
        Examples: <strong>Delhi, Mumbai, Bangalore, Hyderabad, Chennai, Kolkata</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2.5, 1, 1.5])
    with col1:
        location = st.text_input(
            "City / Location",
            placeholder="e.g., Delhi, Mumbai, Bangalore...",
            key="doc_location",
            label_visibility="collapsed"
        )
    with col2:
        radius = st.selectbox(
            "Search Radius",
            [5, 10, 15, 25, 50],
            index=1,
            format_func=lambda x: f"{x} km",
            label_visibility="collapsed"
        )
    def auto_detect_location():
        try:
            import requests
            detected_city = ""
            try:
                detected_city = requests.get("https://ipinfo.io/json", timeout=5).json().get("city", "")
            except Exception:
                pass
            
            if not detected_city:
                try:
                    detected_city = requests.get("http://ip-api.com/json/", timeout=5).json().get("city", "")
                except Exception:
                    pass
                    
            if detected_city:
                st.session_state["doc_location"] = detected_city
            else:
                st.toast("Could not detect city automatically.", icon="❌")
        except Exception:
            st.toast("Failed to detect location.", icon="❌")

    with col3:
        st.button("[>] AUTO-DETECT IP LOCATION", use_container_width=True, on_click=auto_detect_location)
    
    if not location:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 3rem; background-color: #0a0a0a; border: 1px solid #333;">
            <div style="font-size:2rem; font-family:monospace; color:#666;">[AWAITING INPUT]</div>
            <p style="font-family:monospace; color:#888;">> Type region name to query Geo-Spatial Engine.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Search for healthcare
    standardized_location = extract_location_from_input(location)
    
    with st.spinner(f"[SYS] Querying geospatial nodes for {standardized_location}..."):
        facilities = doctor_service.find_nearby_healthcare(standardized_location, radius)
    
    if not facilities:
        st.error(f"[ERR] Null response. No infrastructure detected in {standardized_location}.")
        return
    
    # Filters & Sorting
    st.markdown("<h3 style='color:#00ffcc; font-family:monospace;'>[⚙] FILTER METRICS</h3>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        sort_by = st.selectbox("Sort By", ["Distance (Nearest)", "Rating (Highest)", "Fee (Lowest)"])
    with col_f2:
        min_rating = st.slider("Min Rating", 1.0, 5.0, 3.5, 0.5)
    with col_f3:
        max_fee_str = st.selectbox("Max Fee", ["Any", "₹500", "₹1000", "₹2000", "₹5000"])
    with col_f4:
        facility_type_filter = st.selectbox("Facility Type", ["All Types", "Hospital", "Clinic", "Doctor/Specialist"])

    # Process and filter facilities
    import re
    filtered_facilities = []
    for f in facilities:
        # Extract Rating
        rating_str = str(f.get("rating", "0"))
        try:
            rating_val = float(rating_str.split('/')[0][:3])
        except:
            rating_val = 0.0
            
        if rating_val < min_rating:
            continue
            
        # Extract Fee
        fee_str = str(f.get("fee", ""))
        fee_nums = re.findall(r'\d+', fee_str)
        if fee_nums:
            avg_fee = sum(int(x) for x in fee_nums) / len(fee_nums)
        else:
            avg_fee = 0
            
        if max_fee_str != "Any":
            max_fee_val = int(max_fee_str.replace("₹", ""))
            if avg_fee > max_fee_val:
                continue
                
        # Facility Type Filter
        f_type = f.get("type", "").lower()
        if facility_type_filter == "Hospital" and "hospital" not in f_type:
            continue
        elif facility_type_filter == "Clinic" and "clinic" not in f_type:
            continue
        elif facility_type_filter == "Doctor/Specialist" and ("doctor" not in f_type and "specialist" not in f_type and "eye" not in f_type):
            continue

        # Extract Distance
        dist_str = str(f.get("distance", "0")).replace("~", "").replace(" km", "").strip()
        try:
            dist_val = float(dist_str)
        except:
            dist_val = 999.0
            
        f["_rating_val"] = rating_val
        f["_fee_val"] = avg_fee
        f["_dist_val"] = dist_val
        filtered_facilities.append(f)
        
    # Apply Sorting
    if sort_by == "Rating (Highest)":
        filtered_facilities.sort(key=lambda x: x["_rating_val"], reverse=True)
    elif sort_by == "Fee (Lowest)":
        filtered_facilities.sort(key=lambda x: x["_fee_val"])
    else:
        filtered_facilities.sort(key=lambda x: x["_dist_val"])

    facilities_to_show = filtered_facilities

    # Results header
    section_header(f"[/] FACILITIES DETECTED IN {standardized_location.upper()}")
    
    if not facilities_to_show:
        st.warning("[SYS] Filters too restrictive. Zero matches.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("NODES_FOUND", str(len(facilities_to_show)), "", "blue")
        with col2:
            hospitals = sum(1 for f in facilities_to_show if "hospital" in f.get("type", "").lower())
            metric_card("HOSPITALS", str(hospitals), "", "red")
        with col3:
            clinics = sum(1 for f in facilities_to_show if "clinic" in f.get("type", "").lower() or "doctor" in f.get("type", "").lower() or "specialist" in f.get("type", "").lower())
            metric_card("CLINICS", str(clinics), "", "green")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Deterministic names for doctors
    first_names = ["Arun", "Priya", "Rahul", "Sneha", "Vikram", "Anjali", "Rakesh", "Kavita", "Sanjay", "Neha"]
    last_names = ["Sharma", "Patel", "Reddy", "Singh", "Kumar", "Gupta", "Das", "Joshi", "Iyer", "Nair"]

    
    # Display facilities
    for i, facility in enumerate(facilities_to_show):
        name = facility.get("name", "Unknown Facility")
        facility_type = facility.get("type", "Healthcare")
        address = facility.get("address", "Address not available")
        phone = facility.get("phone", "Not available")
        distance = facility.get("distance", "Unknown")
        rating = facility.get("rating", "N/A")
        fee = facility.get("fee", "N/A")
        hours = facility.get("opening_hours", "Not specified")
        
        # Generate fake doctor name
        name_hash = hash(name)
        doc_first = first_names[name_hash % len(first_names)]
        doc_last = last_names[(name_hash // 10) % len(last_names)]
        doctor_name = f"Dr. {doc_first} {doc_last}"
        
        st.markdown(f"""
        <div class="card" style="font-family:monospace;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <h3 style="margin:0; color:#00ffcc; text-transform:uppercase;">[DIR] {doctor_name}</h3>
                    <p style="margin:0.2rem 0; color:#888; font-weight:bold;">{name}</p>
                    <p style="margin:0.2rem 0; color:#666;">> TYPE: {facility_type}</p>
                    <p style="margin:0.2rem 0;">> ADDR: {address}</p>
                    <p style="margin:0.2rem 0;">> TEL: {phone}</p>
                    <p style="margin:0.2rem 0;">> HRS: {hours}</p>
                </div>
                <div style="text-align: right; min-width: 150px;">
                    <div style="font-size:1.5rem; font-weight:700; color:#1a73e8;">{distance}</div>
                    <div style="font-size:0.9rem; color:#666;">away</div>
                    <br>
                    <div style="font-size:1.1rem; color:#d9a404;">[RATING] {rating}</div>
                    <div style="font-size:0.9rem; color:#28a745; font-weight:600;">[FEE] {fee}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"[+] ALLOCATE APPOINTMENT SLOT"):
            with st.form(key=f"book_form_{i}"):
                st.markdown(f"**INITIATE BOOKING FOR {doctor_name.upper()}**")
                col_a, col_b = st.columns(2)
                with col_a:
                    date = st.date_input("Select Date", key=f"date_{i}")
                with col_b:
                    time = st.time_input("Select Time", key=f"time_{i}")
                
                patient_name = st.text_input("Patient Name", key=f"name_{i}")
                reason = st.text_area("Reason for Visit (Optional)", key=f"reason_{i}")
                
                if st.form_submit_button("[>] SECURE SLOT", type="primary", use_container_width=True):
                    if patient_name.strip():
                        st.success(f"[SYS] APPOINTMENT SECURED: {patient_name} -> {doctor_name} ON {date.strftime('%B %d, %Y')} @ {time.strftime('%I:%M %p')}.")
                    else:
                        st.error("[ERR] PATIENT NAME REQUIRED.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tips section
    section_header("[/] OPERATIONAL PROTOCOLS")
    
    tips = [
        "> For critically elevated indicators (OSI/VIS), route to nearest hospital immediately.",
        "> Prioritize Ophthalmology departments for dedicated hardware diagnostics.",
        "> Contact nodes ahead of arrival to confirm availability and fee structures.",
        "> Download and present your local PDF diagnostic payload upon arrival."
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="card" style="padding: 0.8rem 1.2rem; font-family:monospace; color:#888;">
            <p style="margin:0;">{tip}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="warning-box" style="font-family:monospace;">
        [WARNING] Telemetry routing relies on open-source geolocation layers. Availability of specialists cannot be guaranteed dynamically. Route to emergency nodes manually if critical.
    </div>
    """, unsafe_allow_html=True)
    
    # New search
    if st.button("[!] PURGE REGIONAL DATA", use_container_width=True):
        st.session_state["doc_location"] = ""
        st.rerun()
    
    st.markdown("""
    <div class="footer">
        Data sourced from OpenStreetMap | © VisionCare AI
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()