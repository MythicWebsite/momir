"""
Image Handler for processing Magic: The Gathering card images.

This module handles image manipulation for card images including resizing,
enhancing for printing, and creating double-faced card layouts.
"""

from io import BytesIO
from typing import Union, Optional

from PIL import Image, ImageEnhance


def resize_image(img: Image.Image, new_width: int) -> Image.Image:
    """
    Resize an image to a new width while maintaining aspect ratio.
    
    Args:
        img: PIL Image object to resize
        new_width: Target width in pixels
        
    Returns:
        Resized PIL Image object
    """
    width_percent = new_width / img.size[0]
    new_height = int(img.size[1] * width_percent)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)


def convert_card(img_path: str, card_id: Optional[str] = None, img_return: bool = False) -> Union[str, Image.Image]:
    """
    Convert a card image for printing by enhancing contrast, sharpness, and brightness.
    
    Args:
        img_path: Path to the image file or Image object
        card_id: Optional ID for saving the processed image
        img_return: If True, return Image object instead of saving
        
    Returns:
        File path if saved, or PIL Image object if img_return is True
    """
    # Load image
    if isinstance(img_path, str):
        img = Image.open(img_path)
    else:
        img = img_path
    
    # Resize to standard width
    img = resize_image(img, 384)
    
    # Enhance image for better printing
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2.0)
    
    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(6.0)
    
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(4.0)
    
    # Convert to monochrome for printing
    img = img.convert("1")
    
    if img_return:
        return img
    else:
        output_path = f"Images/{card_id}.png"
        img.save(output_path)
        return output_path


def flip_card_image(img1: bytes, img2: bytes, card_id: Optional[str] = None) -> Union[str, bytes]:
    """
    Create a combined image for double-faced cards with the second face rotated 180 degrees.
    
    Args:
        img1: Bytes of the first card face image
        img2: Bytes of the second card face image  
        card_id: Optional ID for saving the combined image
        
    Returns:
        File path if card_id provided, otherwise bytes of the combined image
    """
    # Load images from bytes
    img1_pil = Image.open(BytesIO(img1))
    img2_pil = Image.open(BytesIO(img2))
    
    # Rotate the second image 180 degrees
    img2_pil = img2_pil.rotate(180)

    # Create combined image with padding between faces
    padding = 40
    new_height = img1_pil.height + img2_pil.height + padding
    combo_img = Image.new('RGB', (img1_pil.width, new_height), color='white')

    # Paste images with padding
    combo_img.paste(img1_pil, (0, 0))
    combo_img.paste(img2_pil, (0, img1_pil.height + padding))
    
    if card_id:
        # Save to file
        output_path = f"Images/{card_id}.png"
        combo_img.save(output_path)
        return output_path
    else:
        # Return as bytes
        img_bytes = BytesIO()
        combo_img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()