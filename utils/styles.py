"""
Common CSS styles and UI components for Streamlit pages.
"""
import streamlit as st


def load_css():
    """Load custom CSS styles for the app."""
    st.markdown("""
    <style>
        /* Base Theme Override for Radiology Display */
        .stApp {
            background-color: #000000;
        }
        
        /* Typography & Globals */
        h1, h2, h3, h4, h5 {
            color: #00ffcc;
            font-family: 'Courier New', Courier, monospace;
            text-transform: uppercase;
        }
        
        p, span, div {
            font-family: 'Courier New', Courier, monospace;
        }
        
        .main-header {
            font-size: 2rem;
            font-weight: bold;
            color: #00ffcc;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            letter-spacing: 2px;
        }
        
        .sub-header {
            font-size: 1rem;
            color: #888;
            margin-bottom: 2rem;
            border-left: 2px solid #00ffcc;
            padding-left: 10px;
        }
        
        /* Clinical Cards */
        .card {
            background: rgba(10, 10, 10, 0.8);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0, 255, 204, 0.05), 0 1px 3px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card:hover {
            box-shadow: 0 6px 12px rgba(0, 255, 204, 0.1), 0 2px 4px rgba(0, 0, 0, 0.5);
        }
        .card-butter {
            background: linear-gradient(135deg, rgba(0,255,204,0.1), rgba(0,255,204,0.05));
            border-left: 4px solid #00ffcc;
        }
        .card-green {
            background: linear-gradient(135deg, #28a745, #1e7e34);
            color: white;
        }
        .card-orange {
            background: linear-gradient(135deg, #ff9800, #f57c00);
            color: white;
        }
        .card-red {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
        }
        .card-purple {
            background: linear-gradient(135deg, #6f42c1, #5a32a3);
            color: white;
        }
        
        /* Metric display */
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
            margin: 0;
        }
        
        /* Feature boxes */
        .feature-box {
            background: rgba(18, 18, 18, 0.6);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .feature-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(217, 164, 4, 0.3);
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .feature-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.3rem;
        }
        .feature-desc {
            font-size: 0.85rem;
            color: #aaa;
        }
        
        /* Risk badges */
        .risk-low {
            background: #d4edda;
            color: #155724;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        .risk-medium {
            background: #fff3cd;
            color: #856404;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        .risk-high {
            background: #f8d7da;
            color: #721c24;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        
        /* Section */
        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #d9a404;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #d9a404;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.85rem;
            padding: 2rem 0 1rem 0;
            border-top: 1px solid #eee;
            margin-top: 3rem;
        }
        
        /* Spinner colors */
        .stSpinner > div {
            border-top-color: #d9a404 !important;
        }
        
        /* Button primary */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Info boxes */
        .info-box {
            background: rgba(25, 115, 232, 0.1);
            border-left: 4px solid #1a73e8;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .warning-box {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .success-box {
            background: rgba(40, 167, 69, 0.1);
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .danger-box {
            background: rgba(220, 53, 69, 0.1);
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Typography & Globals Removed Here */
        
        /* Step numbers */
        .step-number {
            background: #d9a404;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 8px;
        }
        
        /* Highlight text */
        .highlight {
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        /* Responsive container */
        @media (max-width: 768px) {
            .main-header { font-size: 1.8rem; }
            .metric-value { font-size: 1.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)


def metric_card(label, value, emoji="📊", color="blue"):
    """Create a styled metric card."""
    color_map = {
        "blue": "card-butter",
        "green": "card-green",
        "orange": "card-orange",
        "red": "card-red",
        "purple": "card-purple"
    }
    card_class = color_map.get(color, "card-butter")
    
    st.markdown(f"""
    <div class="card {card_class}">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p class="metric-label">{label}</p>
                <p class="metric-value">{value}</p>
            </div>
            <div style="font-size: 2.5rem;">{emoji}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def info_message(text, type="info"):
    """Display a styled info/warning/success/danger message."""
    type_map = {
        "info": "info-box",
        "warning": "warning-box",
        "success": "success-box",
        "danger": "danger-box"
    }
    box_class = type_map.get(type, "info-box")
    
    st.markdown(f"""
    <div class="{box_class}">
        {text}
    </div>
    """, unsafe_allow_html=True)


def section_header(title):
    """Display a section header."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def risk_badge(level):
    """Display a risk level badge."""
    level_lower = level.lower() if level else "unknown"
    badge_class = f"risk-{level_lower}" if level_lower in ["low", "medium", "high"] else "risk-low"
    emoji_map = {"low": "✅", "medium": "⚠️", "high": "🚨"}
    emoji = emoji_map.get(level_lower, "❓")
    
    st.markdown(f'<span class="{badge_class}">{emoji} {level.title()}</span>', unsafe_allow_html=True)
