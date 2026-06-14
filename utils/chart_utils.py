"""
Chart utility functions for creating visualizations.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
from datetime import datetime
from config.settings import ASSETS_DIR


# Color scheme
COLORS = {
    "primary": "#1a73e8",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "purple": "#6f42c1",
    "pink": "#e83e8c"
}

RISK_COLORS = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}
BACKGROUND_COLOR = "#f0f2f6"


def set_style():
    """Set consistent style for all charts."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.facecolor'] = BACKGROUND_COLOR
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = '#cccccc'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3


def create_risk_gauge(score, title="Risk Score", filename=None):
    """
    Create a gauge chart for a single risk score.
    
    Args:
        score: Value 0-100
        title: Chart title
        filename: Output filename (optional)
        
    Returns:
        str: Path to saved chart image
    """
    set_style()
    
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Create gauge background
    if score <= 30:
        color = COLORS["success"]
    elif score <= 70:
        color = COLORS["warning"]
    else:
        color = COLORS["danger"]
    
    # Gauge bar
    ax.barh([0], [100], height=0.5, color='#e0e0e0', edgecolor='none')
    ax.barh([0], [score], height=0.5, color=color, edgecolor='none')
    
    # Add score text
    ax.text(score/2, 0, f'{int(score)}', ha='center', va='center', 
            fontsize=24, fontweight='bold', color='white')
    
    # Risk labels
    ax.text(15, -0.8, 'Low', ha='center', fontsize=9, color=COLORS["success"])
    ax.text(50, -0.8, 'Medium', ha='center', fontsize=9, color=COLORS["warning"])
    ax.text(85, -0.8, 'High', ha='center', fontsize=9, color=COLORS["danger"])
    
    # Threshold lines
    ax.axvline(x=30, ymin=0.45, ymax=0.55, color=COLORS["warning"], linewidth=2, linestyle='--', alpha=0.5)
    ax.axvline(x=70, ymin=0.45, ymax=0.55, color=COLORS["danger"], linewidth=2, linestyle='--', alpha=0.5)
    
    ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    plt.tight_layout()
    
    return _save_chart(fig, filename, f"gauge_{title.lower().replace(' ', '_')}")


def create_risk_distribution_chart(risk_distribution, filename=None):
    """
    Create a pie chart showing risk distribution.
    
    Args:
        risk_distribution: Dict with 'Low', 'Medium', 'High' counts
        filename: Output filename
        
    Returns:
        str: Path to saved chart
    """
    set_style()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    labels = list(risk_distribution.keys())
    sizes = [risk_distribution.get(k, 0) for k in labels]
    colors_list = [RISK_COLORS.get(k, '#999999') for k in labels]
    explode = [0.05 if s == max(sizes) else 0 for s in sizes] if sizes else [0, 0, 0]
    
    if sum(sizes) > 0:
        wedges, texts, autotexts = ax.pie(
            sizes, explode=explode, labels=labels, colors=colors_list,
            autopct='%1.1f%%', startangle=90, shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    else:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                fontsize=14, transform=ax.transAxes)
    
    ax.set_title('Risk Distribution Among Patients', fontsize=14, fontweight='bold', pad=20)
    ax.axis('equal')
    
    plt.tight_layout()
    
    return _save_chart(fig, filename, "risk_distribution")


def create_scores_comparison_chart(avg_scores, filename=None):
    """
    Create a bar chart comparing average scores across conditions.
    
    Args:
        avg_scores: Dict with condition: score pairs
        filename: Output filename
        
    Returns:
        str: Path to saved chart
    """
    set_style()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    conditions = list(avg_scores.keys())
    scores = [avg_scores.get(c, 0) for c in conditions]
    
    # Color bars based on score
    colors_list = []
    for score in scores:
        if score <= 30:
            colors_list.append(COLORS["success"])
        elif score <= 70:
            colors_list.append(COLORS["warning"])
        else:
            colors_list.append(COLORS["danger"])
    
    bars = ax.bar(conditions, scores, color=colors_list, edgecolor='white', linewidth=1.5, width=0.6)
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{score:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Average Score', fontsize=11)
    ax.set_title('Average Health Scores by Condition', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticklabels([c.replace('_', ' ').title() for c in conditions], fontsize=10)
    
    # Add threshold lines
    ax.axhline(y=30, color=COLORS["warning"], linestyle='--', alpha=0.5, label='Low/Medium Threshold')
    ax.axhline(y=70, color=COLORS["danger"], linestyle='--', alpha=0.5, label='Medium/High Threshold')
    ax.legend(fontsize=8)
    
    plt.tight_layout()
    
    return _save_chart(fig, filename, "scores_comparison")


def create_monthly_trends_chart(monthly_data, filename=None):
    """
    Create a line chart showing monthly scan trends.
    
    Args:
        monthly_data: Dict with month: count pairs
        filename: Output filename
        
    Returns:
        str: Path to saved chart
    """
    set_style()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    months = list(monthly_data.keys())
    counts = [monthly_data.get(m, 0) for m in months]
    
    if months:
        x = range(len(months))
        ax.plot(x, counts, marker='o', linewidth=2.5, markersize=8, 
                color=COLORS["primary"], markerfacecolor='white', markeredgewidth=2)
        
        # Fill area under curve
        ax.fill_between(x, counts, alpha=0.15, color=COLORS["primary"])
        
        # Add value labels
        for i, count in enumerate(counts):
            ax.text(i, count + 0.3, str(count), ha='center', fontsize=9, fontweight='bold')
        
        ax.set_xticks(x)
        ax.set_xticklabels([m[-2:] for m in months], fontsize=9)  # Show month only
    else:
        ax.text(0.5, 0.5, 'No monthly data available', ha='center', va='center', 
                fontsize=14, transform=ax.transAxes)
    
    ax.set_ylabel('Number of Scans', fontsize=11)
    ax.set_xlabel('Month', fontsize=11)
    ax.set_title('Monthly Scan Trends', fontsize=14, fontweight='bold', pad=15)
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    
    return _save_chart(fig, filename, "monthly_trends")


def create_radar_chart(scores, filename=None):
    """
    Create a radar chart comparing all four health metrics.
    
    Args:
        scores: Dict with anemia, jaundice, redness, inflammation scores
        filename: Output filename
        
    Returns:
        str: Path to saved chart
    """
    set_style()
    
    categories = ['Anemia', 'Jaundice', 'Redness', 'Inflammation']
    values = [scores.get(c.lower(), 0) for c in ['anemia', 'jaundice', 'redness', 'inflammation']]
    
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values += values[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Draw chart
    ax.plot(angles, values, 'o-', linewidth=2, color=COLORS["primary"])
    ax.fill(angles, values, alpha=0.25, color=COLORS["primary"])
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    
    # Set y-axis
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8, color='gray')
    
    # Add colored rings for risk zones
    for i, (start, end, color, alpha) in enumerate([
        (0, 30, COLORS["success"], 0.05),
        (30, 70, COLORS["warning"], 0.05),
        (70, 100, COLORS["danger"], 0.05),
    ]):
        pass  # The fill already shows data
    
    ax.set_title('Health Profile Radar', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    return _save_chart(fig, filename, "radar_chart")


def _save_chart(fig, filename, default_name):
    """Save chart to file and return path."""
    charts_dir = os.path.join(ASSETS_DIR, "charts")
    os.makedirs(charts_dir, exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{default_name}_{timestamp}.png"
    
    filepath = os.path.join(charts_dir, filename)
    fig.savefig(filepath, dpi=100, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
    plt.close(fig)
    
    return filepath


def create_all_dashboard_charts(dashboard_data):
    """Create all charts for the dashboard page."""
    charts = {}
    
    if dashboard_data.get("risk_distribution"):
        charts["risk_distribution"] = create_risk_distribution_chart(dashboard_data["risk_distribution"])
    
    if dashboard_data.get("avg_scores"):
        charts["scores"] = create_scores_comparison_chart(dashboard_data["avg_scores"])
    
    if dashboard_data.get("monthly_trends"):
        charts["monthly_trends"] = create_monthly_trends_chart(dashboard_data["monthly_trends"])
    
    return charts