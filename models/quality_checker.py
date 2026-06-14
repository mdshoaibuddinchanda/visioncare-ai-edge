"""
Image quality checking using OpenCV.
Checks for blur, brightness, and contrast.
"""
import cv2
import numpy as np
from PIL import Image
import io


def check_image_quality(image_bytes):
    """
    Check the quality of an uploaded eye image.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        dict: Quality assessment result
    """
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {
                "status": "poor",
                "score": 0,
                "message": "❌ Could not decode image. Please upload a valid eye image.",
                "details": {}
            }
        
        height, width = img.shape[:2]
        
        # 1. Check Blur using Laplacian variance
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_score = min(100, (laplacian_var / 500) * 100)
        is_blurry = laplacian_var < 100
        
        # 2. Check Brightness
        brightness = np.mean(gray)
        brightness_score = 100
        brightness_message = "Good"
        if brightness < 50:
            brightness_score = max(0, (brightness / 50) * 100)
            brightness_message = "Too dark"
        elif brightness > 220:
            brightness_score = max(0, ((255 - brightness) / 35) * 100)
            brightness_message = "Too bright"
        
        # 3. Check Contrast
        contrast = gray.std()
        contrast_score = min(100, (contrast / 60) * 100)
        low_contrast = contrast < 30
        
        # 4. Check if image contains eye (basic check - at least 100x100)
        min_dimension = min(height, width)
        size_ok = min_dimension >= 100
        size_score = min(100, (min_dimension / 500) * 100) if size_ok else max(0, (min_dimension / 100) * 50)
        
        # Calculate overall quality score
        weights = {
            "blur": 0.35,
            "brightness": 0.25,
            "contrast": 0.20,
            "size": 0.20
        }
        
        quality_score = (
            weights["blur"] * (100 - abs(50 - blur_score)) +
            weights["brightness"] * brightness_score +
            weights["contrast"] * contrast_score +
            weights["size"] * size_score
        )
        
        # Determine status
        if quality_score >= 60 and not is_blurry and not low_contrast:
            status = "good"
            message = "✅ Image quality is good. Proceeding with analysis..."
        elif quality_score >= 30:
            status = "fair"
            message = "⚠️ Image quality is acceptable but could be better. Analysis may have reduced accuracy."
        else:
            status = "poor"
            message = "❌ Poor image quality. Please retake the photo with better lighting and focus."
        
        details = {
            "blur_score": round(blur_score, 1),
            "is_blurry": bool(is_blurry),
            "brightness": round(float(brightness), 1),
            "brightness_status": brightness_message,
            "contrast": round(float(contrast), 1),
            "contrast_score": round(contrast_score, 1),
            "low_contrast": bool(low_contrast),
            "dimensions": f"{width}x{height}",
            "size_ok": bool(size_ok)
        }
        
        return {
            "status": status,
            "score": round(quality_score, 1),
            "message": message,
            "details": details
        }
        
    except Exception as e:
        return {
            "status": "error",
            "score": 0,
            "message": f"❌ Error checking image quality: {str(e)}",
            "details": {}
        }