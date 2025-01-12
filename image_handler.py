from PIL import Image, ImageEnhance
import numpy as np
from io import BytesIO

def resize_image(img: Image, new_width: int):
    """Resizes an image to a new width while maintaining the aspect ratio."""
    width_percent = new_width / img.size[0]
    new_height = int(img.size[1] * width_percent)
    return img.resize((new_width, new_height))

def convert_card(img: bytes, card_id: str) -> bytes:
    """Converts a card image to a black and white image."""
    img = Image.open(BytesIO(img))
    img = resize_image(img, 384)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert("1")
    img.save(f"Images/{card_id}.png")
    return f"Images/{card_id}.png"

def flip_card_image(img: bytes, img2: bytes, card_id: str) -> bytes:
    """Flips the card image to create a double sided card."""
    img = Image.open(BytesIO(img))
    img2 = Image.open(BytesIO(img2))
    img = resize_image(img, 384)
    img2 = resize_image(img2, 384)
    img2 = img2.rotate(180)

    new_height = img.height + img2.height + 10
    combo_img = Image.new('RGB', (img.width, new_height), color='white')

    combo_img.paste(img, (0, 0))
    combo_img.paste(img2, (0, img.height + 10))
    img_bytes = BytesIO()
    combo_img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()
    
