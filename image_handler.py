from PIL import Image, ImageEnhance
import numpy as np
from io import BytesIO

def floyd_steinberg_dither(img: Image):
    """Applies Floyd-Steinberg dithering to a grayscale image."""

    img_array = np.array(img)

    for y in range(img_array.shape[0] - 1):
        for x in range(img_array.shape[1] - 1):
            old_pixel = img_array[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            img_array[y, x] = new_pixel
            error = old_pixel - new_pixel

            img_array[y, x + 1] += error * 7 / 16
            img_array[y + 1, x - 1] += error * 3 / 16
            img_array[y + 1, x] += error * 5 / 16
            img_array[y + 1, x + 1] += error * 1 / 16

    return Image.fromarray(img_array)

def resize_image(img: Image, new_width: int):
    """Resizes an image to a new width while maintaining the aspect ratio."""
    width_percent = new_width / img.size[0]
    new_height = int(img.size[1] * width_percent)
    return img.resize((new_width, new_height))

def convert_card(img: bytes, card_id: str) -> bytes:
    """Converts a card image to a black and white image."""
    img = Image.open(BytesIO(img))
    img = resize_image(img, 400)
    # img = img.convert("L")
    # img = floyd_steinberg_dither(img)
    # fn = lambda x : 255 if x > 154 else 0
    # img = img.convert('L').point(fn, mode='1')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert("1")
    img.save(f"Images/{card_id}.png")
    return f"Images/{card_id}.png"
