from tkinter import image_names
from typing import Tuple
from PIL import Image

def help_expand_image(img: Image, min_width: int, min_height: int) -> Image:
    if img.width < min_width or img.height < min_height:
        width, height = img.size
        while True:
            width += 1
            height = img.height * width // img.width
            if width >= min_width and height >= min_height:
                break
        img = img.resize((width, height), Image.LANCZOS)
    return img

def help_shrink_image(img: Image, max_width: int, max_height: int) -> Image:
    if img.width > max_width or img.height > max_height:
        width, height = img.size
        while True:
            width -= 1
            height = img.height * width // img.width
            if width <= max_width and height <= max_height:
                break
        img = img.resize((width, height), Image.LANCZOS)
    return img

