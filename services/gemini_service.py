"""
Gemini Vision API service for eye image analysis.
"""
import os
import json
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
import PIL.Image


class GeminiService:
    """Handles communication with Google Gemini Vision API."""
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_eye(self, image_path, prompt):
        """
        Send an eye image to Gemini for analysis.
        """
        if not self.api_key:
            return {
                "status": "error",
                "response": "",
                "message": "GEMINI_API_KEY not configured. Set it in .env file."
            }
        
        if not self.model:
            return {
                "status": "error",
                "response": "",
                "message": "Gemini model not initialized. Check your API key."
            }
        
        try:
            # Open and prepare the image
            img = PIL.Image.open(image_path)
            
            # Generate response
            response = self.model.generate_content([prompt, img])
            
            return {
                "status": "success",
                "response": response.text if response else "",
                "message": "Analysis completed successfully."
            }
            
        except Exception as e:
            error_msg = str(e)
            if "API_KEY" in error_msg.upper() or "API key" in error_msg:
                return {
                    "status": "error",
                    "response": "",
                    "message": "Invalid API key. Please check your GEMINI_API_KEY in .env file."
                }
            elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return {
                    "status": "error",
                    "response": "",
                    "message": "API quota exceeded. Please try again later."
                }
            else:
                return {
                    "status": "error",
                    "response": "",
                    "message": f"Gemini API error: {error_msg}"
                }
    
    def generate_text(self, prompt, system_prompt=""):
        """Generate text response using Gemini API."""
        if not self.model:
            return {"status": "error", "response": "Model not initialized"}
        
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            response = self.model.generate_content(full_prompt)
            return {
                "status": "success",
                "response": response.text if response else ""
            }
        except Exception as e:
            return {"status": "error", "response": f"Gemini Error: {str(e)}"}
    
    def is_available(self):
        """Check if Gemini service is configured and working."""
        return self.api_key is not None and len(self.api_key) > 0 and self.model is not None
