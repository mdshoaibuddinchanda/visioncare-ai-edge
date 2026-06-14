"""
PDF utility functions.
"""
import os
from datetime import datetime


def get_report_filename(prefix="VisionCare_Report"):
    """Generate a unique report filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pdf"


def get_latest_report(directory=None):
    """Get the most recently generated report."""
    from config.settings import REPORT_DIR
    dir_path = directory or REPORT_DIR
    
    if not os.path.exists(dir_path):
        return None
    
    pdf_files = [f for f in os.listdir(dir_path) if f.endswith('.pdf')]
    if not pdf_files:
        return None
    
    pdf_files.sort(reverse=True)
    return os.path.join(dir_path, pdf_files[0])


def format_report_size(filepath):
    """Format PDF file size for display."""
    try:
        size_bytes = os.path.getsize(filepath)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    except:
        return "Unknown"