"""
Central configuration settings for VisionCare AI.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama").lower()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:3b")

# Database
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "visioncare.db")

# Paths
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "generated")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

# Risk Thresholds
RISK_LOW_MAX = 30
RISK_MEDIUM_MAX = 70
RISK_HIGH_MAX = 100

# Image Quality
QUALITY_BLUR_THRESHOLD = 100.0
QUALITY_MIN_BRIGHTNESS = 50
QUALITY_MAX_BRIGHTNESS = 240
QUALITY_MIN_CONTRAST = 30

# App
APP_TITLE = "VisionCare AI"
APP_ICON = "👁️"
APP_LAYOUT = "wide"
PAGE_TITLE = "VisionCare AI - AI-Powered Eye Health Screening"
