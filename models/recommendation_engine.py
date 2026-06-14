"""
Generates health, nutrition, and lifestyle recommendations based on analysis results.
"""
from models.risk_classifier import classify_risk


class RecommendationEngine:
    """Creates personalized nutrition, lifestyle, and medical recommendations."""
    
    @staticmethod
    def get_all_recommendations(analysis):
        """
        Generate comprehensive recommendations from analysis data.
        
        Args:
            analysis: Dict from health_predictor
            
        Returns:
            dict: Structured recommendations
        """
        return {
            "nutrition": RecommendationEngine._get_nutrition_advice(analysis),
            "lifestyle": RecommendationEngine._get_lifestyle_advice(analysis),
            "medical": RecommendationEngine._get_medical_advice(analysis),
            "follow_up": RecommendationEngine._get_follow_up_advice(analysis)
        }
    
    @staticmethod
    def _get_nutrition_advice(analysis):
        """Generate nutrition advice based on risk scores."""
        anemia_score = analysis.get("anemia_score", 0)
        jaundice_score = analysis.get("jaundice_score", 0)
        inflammation_score = analysis.get("inflammation_score", 0)
        
        suggestions = []
        warnings = []
        
        # Anemia-related nutrition
        if anemia_score > 30:
            suggestions.extend([
                "🥩 Iron-rich foods: Spinach, lentils, red meat, fortified cereals",
                "🫐 Vitamin C sources: Citrus fruits, bell peppers, tomatoes (enhances iron absorption)",
                "🥚 Protein-rich foods: Eggs, chicken, fish, beans",
                "🌿 Folate-rich foods: Leafy greens, asparagus, Brussels sprouts"
            ])
            if anemia_score > 70:
                warnings.append("⚠️ High anemia risk detected. Consider iron supplementation after consulting a doctor.")
        else:
            suggestions.append("🥗 Continue your balanced diet rich in iron and vitamins")
        
        # Jaundice-related nutrition
        if jaundice_score > 30:
            suggestions.extend([
                "💧 Increase water intake to support liver function (8-10 glasses/day)",
                "🥬 Liver-friendly foods: Beetroot, carrots, leafy greens",
                "🍋 Include antioxidant-rich foods: Berries, nuts, green tea",
                "🚫 Avoid alcohol, fried foods, and processed foods"
            ])
            if jaundice_score > 70:
                warnings.append("🚨 High jaundice risk. Seek immediate medical consultation for liver function tests.")
        
        # Inflammation-related nutrition
        if inflammation_score > 30:
            suggestions.extend([
                "🐟 Omega-3 rich foods: Salmon, mackerel, walnuts, flaxseeds",
                "🍍 Anti-inflammatory foods: Turmeric, ginger, pineapple, green leafy vegetables",
                "🫐 Antioxidant-rich berries: Blueberries, strawberries, acai"
            ])
        
        # General nutrition
        suggestions.extend([
            "🥕 Vitamin A for eye health: Carrots, sweet potatoes, pumpkin, eggs",
            "🥦 Stay hydrated and maintain a colorful plate with diverse vegetables"
        ])
        
        return {
            "suggestions": suggestions,
            "warnings": warnings,
            "summary": "Focus on a nutrient-rich diet with plenty of vegetables, fruits, and lean proteins."
        }
    
    @staticmethod
    def _get_lifestyle_advice(analysis):
        """Generate lifestyle recommendations."""
        overall = analysis.get("overall_health", "good")
        
        advice = [
            "👁️ Follow the 20-20-20 rule: Every 20 mins, look at something 20 feet away for 20 seconds",
            "😴 Get 7-8 hours of quality sleep for eye recovery and overall health",
            "🕶️ Wear UV-protective sunglasses when outdoors",
            "💻 Use blue light filters on digital devices, especially at night",
            "🧴 Avoid rubbing your eyes to prevent irritation and infection",
            "🚭 Avoid smoking as it increases risk of cataracts and macular degeneration",
            "🏃 Exercise regularly to maintain healthy blood circulation to the eyes"
        ]
        
        if overall == "poor":
            advice.insert(0, "🏥 Schedule an appointment with an ophthalmologist immediately")
        elif overall == "moderate":
            advice.insert(0, "📅 Consider scheduling a routine eye check-up within the next week")
        
        return advice
    
    @staticmethod
    def _get_medical_advice(analysis):
        """Generate medical consultation advice."""
        urgent = analysis.get("urgent_care_needed", False)
        advice = analysis.get("doctor_consultation_advice", "")
        
        # Determine which specialists to see
        specialists = []
        
        if analysis.get("anemia_score", 0) > 50:
            specialists.append("🩺 General Physician / Hematologist (for anemia evaluation)")
        if analysis.get("jaundice_score", 0) > 50:
            specialists.append("🏥 Hepatologist / Gastroenterologist (for liver function evaluation)")
        if analysis.get("redness_score", 0) > 50:
            specialists.append("👁️ Ophthalmologist (for eye redness evaluation)")
        if analysis.get("inflammation_score", 0) > 50:
            specialists.append("👁️ Ophthalmologist (for eye inflammation evaluation)")
        
        if not specialists:
            specialists.append("👁️ Routine eye check-up with an optometrist is recommended annually")
        
        return {
            "urgent": urgent,
            "message": advice,
            "specialists": specialists,
            "general_advice": "Keep a record of your symptoms and share this report with your healthcare provider."
        }
    
    @staticmethod
    def _get_follow_up_advice(analysis):
        """Generate follow-up recommendations."""
        scores = {
            "anemia": analysis.get("anemia_score", 0),
            "jaundice": analysis.get("jaundice_score", 0),
            "redness": analysis.get("redness_score", 0),
            "inflammation": analysis.get("inflammation_score", 0)
        }
        
        max_score = max(scores.values())
        
        if max_score > 70:
            interval = "1-2 weeks"
            priority = "High - Immediate"
        elif max_score > 30:
            interval = "1 month"
            priority = "Medium - Soon"
        else:
            interval = "3-6 months"
            priority = "Low - Routine"
        
        return {
            "recommended_interval": interval,
            "priority": priority,
            "next_scan_advice": f"Recommended to take another scan in {interval} to monitor changes.",
            "symptoms_to_watch": [
                "Blurred or decreased vision",
                "Eye pain or discomfort",
                "Persistent redness or discharge",
                "Yellowing of skin or eyes",
                "Extreme fatigue or paleness",
                "Headaches or eye strain"
            ]
        }