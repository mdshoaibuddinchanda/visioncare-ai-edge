"""
PDF report generation service using ReportLab.
"""
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from config.settings import REPORT_DIR, ASSETS_DIR


class PDFService:
    """Generates PDF health reports for patients."""
    
    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a73e8'),
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#444444'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#1a73e8'),
            spaceBefore=12,
            spaceAfter=6,
            borderWidth=0,
            borderColor=HexColor('#1a73e8')
        ))
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#333333'),
            spaceBefore=8,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='BodyText2',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#444444'),
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
        self.styles.add(ParagraphStyle(
            name='ScoreBig',
            parent=self.styles['Normal'],
            fontSize=28,
            textColor=HexColor('#1a73e8'),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#888888'),
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#cc0000'),
            alignment=TA_CENTER,
            spaceBefore=12
        ))
    
    def generate_report(self, patient_info, image_path, analysis, recommendations, risk_classifications, output_filename=None):
        """
        Generate a PDF health report.
        
        Args:
            patient_info: Dict with name, age, gender
            image_path: Path to the uploaded eye image
            analysis: Analysis results dict
            recommendations: Recommendations dict
            risk_classifications: Risk classification dict
            output_filename: Custom filename (optional)
            
        Returns:
            str: Path to generated PDF
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"VisionCare_Report_{timestamp}.pdf"
        
        output_path = os.path.join(REPORT_DIR, output_filename)
        
        # Build document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=20*mm,
            bottomMargin=20*mm,
            leftMargin=15*mm,
            rightMargin=15*mm
        )
        
        story = []
        
        # Header
        story.append(Paragraph("👁️ VisionCare AI", self.styles['ReportTitle']))
        story.append(Paragraph("AI-Powered Eye Health Screening Report", self.styles['SubTitle']))
        story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#1a73e8')))
        story.append(Spacer(1, 10))
        
        # Report metadata
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", self.styles['BodyText2']))
        story.append(Paragraph(f"<b>Report ID:</b> VCR-{datetime.now().strftime('%y%m%d')}-{hash(output_filename) % 10000:04d}", self.styles['BodyText2']))
        story.append(Spacer(1, 12))
        
        # Section 1: Patient Information
        story.append(Paragraph("📋 Patient Information", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc')))
        
        patient_data = [
            ["Name", patient_info.get("name", "Anonymous")],
            ["Age", str(patient_info.get("age", "N/A"))],
            ["Gender", patient_info.get("gender", "Not specified")],
            ["Scan Date", datetime.now().strftime("%Y-%m-%d %H:%M")]
        ]
        
        patient_table = Table(patient_data, colWidths=[120, 350])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1a73e8')),
            ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#333333')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 12))
        
        # Section 2: Eye Image
        if image_path and os.path.exists(image_path):
            story.append(Paragraph("📸 Scan Image", self.styles['SectionHeader']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc')))
            try:
                img = Image(image_path, width=200, height=150)
                story.append(img)
            except:
                story.append(Paragraph("<i>Image preview unavailable</i>", self.styles['BodyText2']))
            story.append(Spacer(1, 12))
        
        # Section 3: Health Assessment Scores
        story.append(Paragraph("🏥 Health Assessment Scores", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc')))
        
        scores_data = [["Condition", "Score (0-100)", "Risk Level", "Status"]]
        
        conditions = [
            ("Anemia Risk", analysis.get("anemia_score", 0), risk_classifications.get("anemia", {})),
            ("Jaundice Risk", analysis.get("jaundice_score", 0), risk_classifications.get("jaundice", {})),
            ("Eye Redness", analysis.get("redness_score", 0), risk_classifications.get("redness", {})),
            ("Inflammation", analysis.get("inflammation_score", 0), risk_classifications.get("inflammation", {}))
        ]
        
        for name, score, risk in conditions:
            color = risk.get("color", "gray")
            emoji = risk.get("emoji", "❓")
            scores_data.append([
                name,
                str(int(score)),
                f"{emoji} {risk.get('level', 'Unknown')}",
                risk.get('label', '')
            ])
        
        scores_table = Table(scores_data, colWidths=[140, 80, 120, 180])
        scores_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5f5')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 8))
        
        # Overall Health
        overall = risk_classifications.get("overall", {})
        story.append(Paragraph(
            f"<b>Overall Health Status:</b> {overall.get('emoji', '')} {overall.get('label', 'Analysis Incomplete')}",
            self.styles['BodyText2']
        ))
        story.append(Spacer(1, 12))
        
        # Section 4: Detailed Explanations
        story.append(Paragraph("📝 Detailed Analysis", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc')))
        
        explanations = [
            ("Anemia", analysis.get("anemia_explanation", "")),
            ("Jaundice", analysis.get("jaundice_explanation", "")),
            ("Eye Redness", analysis.get("redness_explanation", "")),
            ("Inflammation", analysis.get("inflammation_explanation", ""))
        ]
        
        for condition, explanation in explanations:
            if explanation:
                story.append(Paragraph(f"<b>{condition}:</b> {explanation}", self.styles['BodyText2']))
        
        if analysis.get("additional_findings") and analysis["additional_findings"] != "None":
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Additional Findings:</b> {analysis['additional_findings']}", self.styles['BodyText2']))
        
        story.append(Spacer(1, 12))
        
        # Section 5: Recommendations
        story.append(Paragraph("💡 Recommendations", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc')))
        
        if recommendations:
            # Nutrition
            nutrition = recommendations.get("nutrition", {})
            if nutrition:
                story.append(Paragraph("🥗 <b>Nutrition Advice</b>", self.styles['SubHeader']))
                for suggestion in nutrition.get("suggestions", []):
                    story.append(Paragraph(f"• {suggestion}", self.styles['BodyText2']))
                for warning in nutrition.get("warnings", []):
                    story.append(Paragraph(f"{warning}", self.styles['BodyText2']))
            
            # Lifestyle
            lifestyle = recommendations.get("lifestyle", [])
            if lifestyle:
                story.append(Paragraph("🏃 <b>Lifestyle Recommendations</b>", self.styles['SubHeader']))
                for rec in lifestyle:
                    story.append(Paragraph(f"• {rec}", self.styles['BodyText2']))
            
            # Medical
            medical = recommendations.get("medical", {})
            if medical:
                story.append(Paragraph("🏥 <b>Medical Consultation</b>", self.styles['SubHeader']))
                if medical.get("urgent"):
                    story.append(Paragraph("🚨 <b>URGENT: Immediate medical attention recommended!</b>", self.styles['BodyText2']))
                if medical.get("message"):
                    story.append(Paragraph(f"• {medical['message']}", self.styles['BodyText2']))
                for specialist in medical.get("specialists", []):
                    story.append(Paragraph(f"• {specialist}", self.styles['BodyText2']))
            
            # Follow-up
            follow_up = recommendations.get("follow_up", {})
            if follow_up:
                story.append(Paragraph("📅 <b>Follow-up Schedule</b>", self.styles['SubHeader']))
                story.append(Paragraph(f"• Priority: {follow_up.get('priority', 'Routine')}", self.styles['BodyText2']))
                story.append(Paragraph(f"• Next scan recommended in: {follow_up.get('recommended_interval', '3-6 months')}", self.styles['BodyText2']))
                if follow_up.get("symptoms_to_watch"):
                    story.append(Paragraph("<b>Symptoms to monitor:</b>", self.styles['BodyText2']))
                    for symptom in follow_up["symptoms_to_watch"][:4]:
                        story.append(Paragraph(f"• {symptom}", self.styles['BodyText2']))
        
        story.append(Spacer(1, 20))
        
        # Disclaimer
        story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cccccc')))
        story.append(Paragraph(
            "<b>⚠️ DISCLAIMER:</b> This report is generated by AI for screening purposes only and is not a medical diagnosis. "
            "VisionCare AI is a preliminary screening tool and should not replace professional medical advice, "
            "diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.",
            self.styles['Disclaimer']
        ))
        story.append(Spacer(1, 10))
        
        # Footer
        story.append(Paragraph(
            f"Generated by VisionCare AI | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Footer']
        ))
        story.append(Paragraph(
            "© 2025 VisionCare AI - AI-Powered Eye Health for Everyone",
            self.styles['Footer']
        ))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def generate_summary_text(self, analysis, risk_classifications):
        """Generate a plain text summary for display."""
        overall = risk_classifications.get("overall", {})
        
        lines = []
        lines.append("=" * 50)
        lines.append("VISIONCARE AI - HEALTH SCREENING SUMMARY")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Overall Status: {overall.get('emoji', '')} {overall.get('label', 'N/A')}")
        lines.append("")
        lines.append("Risk Scores:")
        lines.append(f"  • Anemia: {analysis.get('anemia_score', 0)}/100 - {risk_classifications.get('anemia', {}).get('level', 'N/A')}")
        lines.append(f"  • Jaundice: {analysis.get('jaundice_score', 0)}/100 - {risk_classifications.get('jaundice', {}).get('level', 'N/A')}")
        lines.append(f"  • Eye Redness: {analysis.get('redness_score', 0)}/100 - {risk_classifications.get('redness', {}).get('level', 'N/A')}")
        lines.append(f"  • Inflammation: {analysis.get('inflammation_score', 0)}/100 - {risk_classifications.get('inflammation', {}).get('level', 'N/A')}")
        lines.append("")
        lines.append("=" * 50)
        lines.append("DISCLAIMER: AI screening only. Consult a doctor for medical advice.")
        lines.append("=" * 50)
        
        return "\n".join(lines)
