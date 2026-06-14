"""
About page - Hackathon pitch and project information.
"""
import streamlit as st
from utils.styles import load_css, section_header


def show():
    """Display the about page."""
    load_css()
    
    st.markdown('<div class="main-header" style="font-family:monospace; text-transform:uppercase;">[MODULE 06] SYSTEM ARCHITECTURE & MANIFESTO</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header" style="font-family:monospace;">> EDGE COMPUTING DIAGNOSTIC PLATFORM</div>',
        unsafe_allow_html=True
    )
    
    # Problem & Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card" style="min-height: 200px; font-family:monospace;">
            <h3 style="color:#ff0033; margin-top:0;">[!] CRITICAL INFRASTRUCTURE FAILURE</h3>
            <ul style="color:#888; line-height:1.8;">
                <li>Rural sectors lack access to dedicated diagnostic hardware.</li>
                <li>Systemic diseases (anemia, jaundice) remain undetected until critical phases.</li>
                <li>Cloud-dependent AI violates local medical privacy regulations.</li>
                <li>High latency internet prevents rural tele-medicine deployment.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="min-height: 200px; font-family:monospace;">
            <h3 style="color:#00ffcc; margin-top:0;">[>] THE EDGE SOLUTION</h3>
            <ul style="color:#888; line-height:1.8;">
                <li>Deploy massive parameter VLM models strictly to local offline terminals.</li>
                <li>Extract 4 biological health indicators strictly via optical telemetry.</li>
                <li>Execute secure AES-256 peer-to-peer database synchronization.</li>
                <li>Operate autonomously without cloud latency or subscription fees.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # The Pitch
    section_header("[/] ARCHITECTURAL OVERVIEW")
    
    st.markdown("""
    <div class="card" style="border-left: 4px solid #00ffcc; background-color: #0a0a0a; padding: 2rem; font-family:monospace;">
        <h3 style="color:#00ffcc; margin-top:0;">VisionCare AI operates as an offline Edge Diagnostic Terminal.</h3>
        <p style="font-size:1rem; line-height:1.8; color:#aaa;">
        It fuses local Qwen2.5-VL optical inference with dynamic conversational triage (LLMs) to accurately extract 
        <strong>CPI (Pallor), SIR (Icterus), VIS (Redness), and OSI (Inflammation)</strong> telemetry entirely on the edge. 
        It integrates localized geospatial logic to route critical anomalies to the nearest OpenStreetMap medical node.
        </p>
        <p style="font-size:0.9rem; color:#888; margin-top:1rem;">
        <em>> ZERO CLOUD DEPENDENCY. ZERO PRIVACY LEAKS.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How It Works
    section_header("[/] EXECUTION PIPELINE")
    
    tech_steps = [
        ("[01]", "DATA INGESTION", "Optical payload uploaded via secure terminal interface."),
        ("[02]", "EDGE INFERENCE", "Local Vision-Language Model calculates risk vectors."),
        ("[03]", "DATA FUSION", "Image matrices fused with LLM conversational triage history."),
        ("[04]", "REPORT COMPILE", "Secure offline PDF matrix generated and signed."),
        ("[05]", "NODE ROUTING", "Geospatial engine queries OpenStreetMap for nearest facility."),
        ("[06]", "DATA SYNC", "WebRTC mesh network initiates CRDT sync across local clinic laptops.")
    ]
    
    for icon, title, desc in tech_steps:
        st.markdown(f"""
        <div class="card" style="padding: 0.8rem 1.5rem; display: flex; align-items: center;">
            <div style="font-size:2rem; margin-right:1rem;">{icon}</div>
            <div>
                <strong style="font-size:1.1rem;">{title}</strong><br>
                <span style="color:#666;">{desc}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Stack
    section_header("🛠️ Technology Stack")
    
    tech_stack = [
        ("Streamlit", "Web framework for rapid UI development", "https://streamlit.io"),
        ("Google Gemini Vision", "AI model for eye image analysis", "https://deepmind.google/gemini"),
        ("OpenCV", "Image quality assessment and preprocessing", "https://opencv.org"),
        ("ReportLab", "PDF report generation", "https://www.reportlab.com"),
        ("SQLite", "Local database for scan history", "https://sqlite.org"),
        ("Matplotlib", "Charts and data visualization", "https://matplotlib.org"),
        ("OpenStreetMap", "Geocoding and healthcare facility search", "https://openstreetmap.org"),
        ("Pillow", "Image processing and enhancement", "https://python-pillow.org")
    ]
    
    cols = st.columns(4)
    for i, (name, desc, url) in enumerate(tech_stack):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="feature-box">
                <div class="feature-title">{name}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Impact
    section_header("🌍 Social Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size:3rem;">🏥</div>
            <h4>Healthcare Access</h4>
            <p style="color:#666; font-size:0.9rem;">
                Brings preliminary health screening to areas with limited medical infrastructure. 
                Users only need a smartphone and internet connection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size:3rem;">💰</div>
            <h4>Zero-Cost Screening</h4>
            <p style="color:#666; font-size:0.9rem;">
                Free health screening eliminates financial barriers. 
                Reduces the need for expensive lab tests for preliminary assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size:3rem;">🌐</div>
            <h4>Community Health</h4>
            <p style="color:#666; font-size:0.9rem;">
                Aggregated anonymized data enables community-level health monitoring 
                and early outbreak detection for public health interventions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Future Roadmap
    section_header("[/] V2 RESEARCH ROADMAP")
    
    roadmap = [
        "> Deploy fully-autonomous WebRTC mesh network layer.",
        "> Implement hardware-accelerated quantization for mobile deployment.",
        "> Integrate WebGL local rendering for 3D eye topography mapping.",
        "> Support real-time RTSP camera feeds with OpenCV frame capture."
    ]
    
    for item in roadmap:
        st.markdown(f"<p style='margin:0.5rem 0; font-size:1.05rem;'>{item}</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team / Credits
    section_header("👥 Team")
    
    st.markdown("""
    <div class="card" style="text-align: center; padding: 2rem;">
        <div style="font-size:4rem;">👁️</div>
        <h3>Built with ❤️ for Devfolio Hackathon</h3>
        <p style="color:#666;">
            VisionCare AI is a hackathon project demonstrating the power of AI 
            for social good. We believe technology should serve everyone, everywhere.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="warning-box" style="font-family:monospace;">
        [WARNING] VisionCare AI operates strictly as a telemetry inference protocol. 
        It does not override or supersede professional medical hardware. 
        Diagnostic outputs are non-deterministic estimations based on parameter matrices.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer" style="font-family:monospace;">
        > VISIONCARE AI EDGE TERMINAL<br>
        > DEVFOLIO HACKATHON 2025<br>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()