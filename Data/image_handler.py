from PIL import Image, ImageEnhance
from io import BytesIO

def resize_image(img: Image, new_width: int):
    width_percent = new_width / img.size[0]
    new_height = int(img.size[1] * width_percent)
    return img.resize((new_width, new_height))

def convert_card(img: str, card_id: str = None, img_return: bool = False) -> bytes:
    img = Image.open(img)
    img = resize_image(img, 384)
    
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)
    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(6)
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(4)
    
    
    img = img.convert("1")
    if not img_return:
        img.save(f"Images/{card_id}.png")
        return f"Images/{card_id}.png"
    else:
        return img

def flip_card_image(img: bytes, img2: bytes, id: str = None) -> bytes:
    img = Image.open(BytesIO(img))
    img2 = Image.open(BytesIO(img2))
    # img = resize_image(img, 384)
    # img2 = resize_image(img2, 384)
    img2 = img2.rotate(180)

    new_height = img.height + img2.height + 40
    combo_img = Image.new('RGB', (img.width, new_height), color='white')

    combo_img.paste(img, (0, 0))
    combo_img.paste(img2, (0, img.height + 40))
    img_bytes = BytesIO()
    combo_img.save(img_bytes, format='PNG')
    if id:
        combo_img.save(f"Images/{id}.png")
        return f"Images/{id}.png"
    else:
        return img_bytes.getvalue()
    