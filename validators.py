"""
Input Validators for Food Calorie Tracker
Validate user inputs for safety and correctness
"""

import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)


def validate_meal_name(name):
    """
    Validate meal name input
    
    Args:
        name (str): Meal name to validate
    
    Returns:
        tuple: (is_valid, message)
    """
    if not name or len(name.strip()) == 0:
        logger.warning("Meal name validation failed: empty input")
        return False, "❌ Meal name cannot be empty"
    
    if len(name) > 100:
        logger.warning(f"Meal name validation failed: too long ({len(name)} chars)")
        return False, "❌ Meal name too long (max 100 characters)"
    
    # Check for invalid characters
    if not all(c.isalnum() or c.isspace() or c in '-,' for c in name):
        logger.warning(f"Meal name validation failed: invalid characters in '{name}'")
        return False, "❌ Invalid characters (only alphanumeric, space, dash, comma allowed)"
    
    logger.info(f"Meal name validated: {name}")
    return True, "✅ Valid"


def validate_calories(calories):
    """
    Validate calories input
    
    Args:
        calories (int/float): Calorie value to validate
    
    Returns:
        tuple: (is_valid, message)
    """
    try:
        cal = int(calories)
    except (ValueError, TypeError):
        logger.warning(f"Calories validation failed: invalid type {type(calories)}")
        return False, "❌ Calories must be a number"
    
    if cal < 0:
        logger.warning("Calories validation failed: negative value")
        return False, "❌ Calories cannot be negative"
    
    if cal == 0:
        logger.warning("Calories validation failed: zero value")
        return False, "❌ Calories must be greater than 0"
    
    if cal > 5000:
        logger.warning(f"Calories validation failed: too high ({cal})")
        return False, "❌ Calories too high (max 5000 kcal)"
    
    logger.info(f"Calories validated: {cal}")
    return True, "✅ Valid"


def validate_image(uploaded_file):
    """
    Validate uploaded image file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        tuple: (is_valid, message)
    """
    if uploaded_file is None:
        logger.warning("Image validation failed: no file")
        return False, "❌ No image selected"
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024
    if uploaded_file.size > max_size:
        logger.warning(f"Image validation failed: file too large ({uploaded_file.size} bytes)")
        return False, f"❌ File too large (max 10MB, got {uploaded_file.size / 1024 / 1024:.1f}MB)"
    
    # Check file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if uploaded_file.type not in allowed_types:
        logger.warning(f"Image validation failed: invalid type {uploaded_file.type}")
        return False, f"❌ Invalid file type: {uploaded_file.type}. Allowed: JPG, PNG"
    
    # Try to open and verify image
    try:
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        img.verify()
        logger.info(f"Image validated: {uploaded_file.name} ({uploaded_file.size} bytes)")
        return True, "✅ Valid"
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}", exc_info=True)
        return False, f"❌ Corrupted image: {str(e)}"
