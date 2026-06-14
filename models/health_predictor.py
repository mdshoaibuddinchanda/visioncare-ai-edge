"""
Core AI health prediction module using Gemini Vision and Local VLMs.
Processes eye images and returns health scores.
"""
import json
import re
import traceback
from config.prompts import EYE_ANALYSIS_PROMPT
from config.settings import AI_PROVIDER
from services.gemini_service import GeminiService
from services.ollama_service import OllamaService


class HealthPredictor:
    """Predicts eye health conditions from uploaded images."""
    
    def __init__(self):
        self.gemini = GeminiService()
        self.ollama = OllamaService()
    
    def analyze_eye_image(self, image_path, patient_history=None):
        """
        Analyze an eye image using AI.
        
        Args:
            image_path: Path to the uploaded image file
            patient_history: Optional text containing patient medical history
            
        Returns:
            dict: Analysis results with scores and explanations
        """
        try:
            prompt = EYE_ANALYSIS_PROMPT
            if patient_history:
                prompt += f"\n\nCRITICAL PATIENT MEDICAL HISTORY:\n{patient_history}\n\nYou MUST factor this history into your final diagnosis and scores. If the patient indicates abnormal appearance, lack of sleep, or diabetes, increase the risk scores accordingly."
                
            if AI_PROVIDER == "ollama":
                result = self.ollama.analyze_eye(image_path, prompt)
            else:
                result = self.gemini.analyze_eye(image_path, prompt)
            
            if result.get("status") == "error":
                return self._fallback_analysis()
            
            analysis_text = result.get("response", "")
            analysis = {}
            
            # Try to extract JSON from the response
            try:
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = analysis_text[json_start:json_end]
                    analysis = json.loads(json_str)
                else:
                    # Dirty regex fallback if no JSON braces found
                    analysis = self._regex_fallback(analysis_text)
                    
            except json.JSONDecodeError:
                # If JSON fails (e.g. cut off), try regex extraction
                analysis = self._regex_fallback(analysis_text)
            
            # Automatically backfill any missing fields (vital for smaller VLMs like moondream)
            analysis["anemia_score"] = analysis.get("anemia_score", 0)
            analysis["jaundice_score"] = analysis.get("jaundice_score", 0)
            analysis["redness_score"] = analysis.get("redness_score", 0)
            analysis["inflammation_score"] = analysis.get("inflammation_score", 0)
            analysis["overall_health"] = analysis.get("overall_health", "unknown")
            
            # Ensure scores are within bounds
            score_fields = ["anemia_score", "jaundice_score", "redness_score", "inflammation_score"]
            for field in score_fields:
                try:
                    val = int(analysis.get(field, 0))
                except (ValueError, TypeError):
                    val = 0
                analysis[field] = max(0, min(100, val))
            
            return analysis
            
        except Exception as e:
            print(f"Error in health prediction: {str(e)}")
            traceback.print_exc()
            return self._fallback_analysis()
            
    def _regex_fallback(self, text):
        """Extract scores from plain text if JSON parsing completely fails."""
        data = {}
        
        # Try to find scores
        for condition in ["anemia", "jaundice", "redness", "inflammation"]:
            match = re.search(rf"{condition}[_\s]*score[\"\'\s:]*(\d+)", text, re.IGNORECASE)
            if match:
                data[f"{condition}_score"] = int(match.group(1))
            else:
                data[f"{condition}_score"] = 0
                
        # Try to find overall health
        if "good" in text.lower() or "healthy" in text.lower():
            data["overall_health"] = "good"
        elif "poor" in text.lower() or "bad" in text.lower() or "urgent" in text.lower():
            data["overall_health"] = "poor"
        else:
            data["overall_health"] = "moderate"
            
        data["additional_findings"] = text[:200] + "..." if len(text) > 200 else text
        return data
    
    def _fallback_analysis(self):
        """Return a safe fallback analysis when AI completely fails."""
        return {
            "anemia_score": 0,
            "anemia_explanation": "Analysis unavailable. Please try again with a clearer image.",
            "jaundice_score": 0,
            "jaundice_explanation": "Analysis unavailable. Please try again with a clearer image.",
            "redness_score": 0,
            "redness_explanation": "Analysis unavailable. Please try again with a clearer image.",
            "inflammation_score": 0,
            "inflammation_explanation": "Analysis unavailable. Please try again with a clearer image.",
            "overall_health": "unknown",
            "additional_findings": "Unable to analyze due to API or connection issue.",
            "dietary_suggestions": [
                "Eat a balanced diet rich in fruits and vegetables",
                "Stay hydrated - drink at least 8 glasses of water daily",
                "Include vitamin A rich foods like carrots and sweet potatoes"
            ],
            "lifestyle_recommendations": [
                "Take regular breaks from screen work (20-20-20 rule)",
                "Get adequate sleep (7-8 hours)",
                "Wear sunglasses in bright sunlight"
            ],
            "urgent_care_needed": False,
            "doctor_consultation_advice": "Consult an ophthalmologist for a comprehensive eye examination.",
            "error": True
        }
