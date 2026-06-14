"""
Converts raw health scores into risk levels (Low, Medium, High).
"""
from config.settings import RISK_LOW_MAX, RISK_MEDIUM_MAX


def classify_risk(score):
    """
    Classify a numeric score into a risk level.
    
    Args:
        score: Numeric score (0-100)
        
    Returns:
        dict: Risk level with label, score range, and color
    """
    if score <= RISK_LOW_MAX:
        return {
            "level": "Low",
            "label": "NOMINAL",
            "color": "green",
            "emoji": "[NOMINAL]",
            "range": "0-30"
        }
    elif score <= RISK_MEDIUM_MAX:
        return {
            "level": "Medium",
            "label": "ELEVATED",
            "color": "orange",
            "emoji": "[ELEVATED]",
            "range": "31-70"
        }
    else:
        return {
            "level": "High",
            "label": "CRITICAL",
            "color": "red",
            "emoji": "[CRITICAL]",
            "range": "71-100"
        }


def classify_all_risks(analysis):
    """
    Classify all health risks from an analysis dict.
    
    Args:
        analysis: Dict containing score fields
        
    Returns:
        dict: Risk classifications for each condition
    """
    return {
        "anemia": classify_risk(analysis.get("anemia_score", 0)),
        "jaundice": classify_risk(analysis.get("jaundice_score", 0)),
        "redness": classify_risk(analysis.get("redness_score", 0)),
        "inflammation": classify_risk(analysis.get("inflammation_score", 0)),
        "overall": classify_overall_risk(analysis.get("overall_health", "unknown"))
    }


def classify_overall_risk(overall_health):
    """
    Classify overall health status.
    
    Args:
        overall_health: String ('good', 'moderate', 'poor', 'unknown')
        
    Returns:
        dict: Risk classification
    """
    mapping = {
        "good": {"level": "Low", "label": "SYSTEM STATUS: NOMINAL", "color": "green", "emoji": "[OK]"},
        "moderate": {"level": "Medium", "label": "SYSTEM STATUS: DEGRADED", "color": "orange", "emoji": "[WARN]"},
        "poor": {"level": "High", "label": "SYSTEM STATUS: CRITICAL FAULT", "color": "red", "emoji": "[ERR]"},
        "unknown": {"level": "Unknown", "label": "SYSTEM STATUS: INCOMPLETE TELEMETRY", "color": "gray", "emoji": "[NULL]"}
    }
    return mapping.get(overall_health, mapping["unknown"])


def get_risk_color(score):
    """Get hex color for a score."""
    if score <= 30:
        return "#28a745"  # Green
    elif score <= 70:
        return "#ffc107"  # Orange
    else:
        return "#dc3545"  # Red