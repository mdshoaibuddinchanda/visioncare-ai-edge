"""
Image utility functions for handling uploads and processing.
"""
import os
import uuid
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
from config.settings import UPLOAD_DIR, PROCESSED_DIR


def save_uploaded_file(uploaded_file, subfolder="uploads"):
    """
    Save an uploaded file to the appropriate directory.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        subfolder: Subfolder name ('uploads' or 'processed')
        
    Returns:
        str: Path to saved file
    """
    base_dir = UPLOAD_DIR if subfolder == "uploads" else PROCESSED_DIR
    os.makedirs(base_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    ext = os.path.splitext(uploaded_file.name)[1] if uploaded_file.name else ".jpg"
    filename = f"eye_{timestamp}_{unique_id}{ext}"
    
    filepath = os.path.join(base_dir, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath


def preprocess_image(image_path, target_size=(512, 512)):
    """
    Preprocess image for AI analysis.
    
    Args:
        image_path: Path to source image
        target_size: Desired output dimensions
        
    Returns:
        str: Path to processed image
    """
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Resize while maintaining aspect ratio
        img.thumbnail(target_size, Image.LANCZOS)
        
        # Create a new image with the target size (padding if needed)
        new_img = Image.new("RGB", target_size, (0, 0, 0))
        paste_x = (target_size[0] - img.size[0]) // 2
        paste_y = (target_size[1] - img.size[1]) // 2
        new_img.paste(img, (paste_x, paste_y))
        
        # Save processed image
        processed_dir = PROCESSED_DIR
        os.makedirs(processed_dir, exist_ok=True)
        
        filename = f"processed_{os.path.basename(image_path)}"
        processed_path = os.path.join(processed_dir, filename)
        new_img.save(processed_path, "JPEG", quality=95)
        
        return processed_path
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return image_path


def enhance_image(image_path):
    """
    Enhance image quality for better analysis.
    
    Args:
        image_path: Path to source image
        
    Returns:
        str: Path to enhanced image
    """
    try:
        img = Image.open(image_path)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        
        # Enhance color
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        
        # Save enhanced image
        processed_dir = PROCESSED_DIR
        os.makedirs(processed_dir, exist_ok=True)
        
        filename = f"enhanced_{os.path.basename(image_path)}"
        enhanced_path = os.path.join(processed_dir, filename)
        img.save(enhanced_path, "JPEG", quality=95)
        
        return enhanced_path
        
    except Exception as e:
        print(f"Error enhancing image: {e}")
        return image_path


def get_image_bytes(image_path):
    """Read image file as bytes."""
    try:
        with open(image_path, "rb") as f:
            return f.read()
    except:
        return None


def get_image_dimensions(image_path):
    """Get image dimensions."""
    try:
        with Image.open(image_path) as img:
            return img.size
    except:
        return (0, 0)