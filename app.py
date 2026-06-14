
"""
VisionCare AI - Main Application
AI-Powered Eye Health Screening & Rural Healthcare Assistant
"""
import streamlit as st
from config.settings import APP_TITLE, APP_ICON, APP_LAYOUT, PAGE_TITLE
from utils.styles import load_css


# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded"
)


def initialize_session():
    """Initialize session state variables."""
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"
    
    if "last_analysis" not in st.session_state:
        st.session_state["last_analysis"] = None
    
    if "last_risks" not in st.session_state:
        st.session_state["last_risks"] = None
    
    if "last_recommendations" not in st.session_state:
        st.session_state["last_recommendations"] = None


def sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Logo / Branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #333; margin-bottom: 1rem;">
            <h2 style="color: #00ffcc; margin: 0; font-family: monospace; letter-spacing: 2px;">VISIONCARE.AI</h2>
            <p style="color: #888; font-size: 0.75rem; margin: 0; font-family: monospace;">CLINICAL DIAGNOSTIC TERMINAL v2.4</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("<h4 style='color: #00ffcc; font-family: monospace; font-size: 0.9rem;'>:: MODULES</h4>", unsafe_allow_html=True)
        
        pages = {
            "[01] DIAGNOSTIC IMAGING": "2_Eye_Scan",
            "[02] CLINICAL REPORTS": "3_Report",
            "[03] SPECIALIST ROUTING": "4_Doctor_Finder",
            "[04] GLOBAL TELEMETRY": "5_Dashboard",
            "[05] SYSTEM INFO": "6_About"
        }
        
        for label, page in pages.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.switch_page(f"pages/{page}.py")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("<h4 style='color: #00ffcc; font-family: monospace; font-size: 0.9rem; margin-top: 1rem;'>:: SYSTEM STATS</h4>", unsafe_allow_html=True)
        from config.settings import AI_PROVIDER
        from services.gemini_service import GeminiService
        from services.ollama_service import OllamaService
        
        # Try to get stats from database
        try:
            from services.database_service import DatabaseService
            db = DatabaseService()
            scan_count = db.get_scan_count()
            patient_count = db.get_patient_count()
            
            st.markdown(f"""
            <div style="background: rgba(0,255,204,0.05); padding: 0.8rem; border-radius: 4px; margin-bottom: 0.5rem; border: 1px solid rgba(0,255,204,0.2);">
                <small style="color:#aaa; font-family:monospace;">SCANS_PROCESSED</small><br>
                <strong style="font-size:1.3rem; color:#00ffcc; font-family:monospace;">{scan_count}</strong>
            </div>
            <div style="background: rgba(0,255,204,0.05); padding: 0.8rem; border-radius: 4px; margin-bottom: 0.5rem; border: 1px solid rgba(0,255,204,0.2);">
                <small style="color:#aaa; font-family:monospace;">PATIENT_RECORDS</small><br>
                <strong style="font-size:1.3rem; color:#00ffcc; font-family:monospace;">{patient_count}</strong>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="background: rgba(0,255,204,0.05); padding: 0.8rem; border-radius: 4px; border: 1px solid rgba(0,255,204,0.2);">
                <small style="color:#888; font-family:monospace;">AWAITING_TELEMETRY</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # AI Status
        st.markdown("<h4 style='color: #00ffcc; font-family: monospace; font-size: 0.9rem; margin-top: 1rem;'>:: ENGINE STATUS</h4>", unsafe_allow_html=True)

        ai_service = OllamaService() if AI_PROVIDER == "ollama" else GeminiService()
        provider_name = "OLLAMA_LOCAL_VISION" if AI_PROVIDER == "ollama" else "GEMINI_API"
        if ai_service.is_available():
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; font-family:monospace;">
                <span style="color:#00ffcc; font-size:1.2rem;">■</span>
                <span style="color:#aaa;">INFERENCE: <span style="color:#00ffcc;">ONLINE</span></span>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"<span style='font-family:monospace; color:#666;'>ENG: {provider_name}</span>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; font-family:monospace;">
                <span style="color:#ff0033; font-size:1.2rem;">■</span>
                <span style="color:#aaa;">INFERENCE: <span style="color:#ff0033;">OFFLINE</span></span>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"<span style='font-family:monospace; color:#666;'>ENG: {provider_name}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; font-size:0.75rem; color:#444; font-family:monospace;">
            STRICTLY CONFIDENTIAL<br>
            UNAUTHORIZED ACCESS PROHIBITED
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    initialize_session()
    
    # Load custom CSS
    load_css()
    
    # Render sidebar
    sidebar()
    
    # Main content area - redirect to Eye Scan page
    st.switch_page("pages/2_Eye_Scan.py")


if __name__ == "__main__":
    main()
