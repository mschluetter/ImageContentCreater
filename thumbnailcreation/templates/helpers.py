from typing import Dict
from PIL import Image

def expand_image_helper(img: Image, min_width: int, min_height: int) -> Image:
    if img.width < min_width or img.height < min_height:
        width, height = img.size
        while True:
            width += 1
            height = img.height * width // img.width
            if width >= min_width and height >= min_height:
                break
        img = img.resize((width, height), Image.LANCZOS)
    return img

def shrink_image_helper(img: Image, max_width: int, max_height: int) -> Image:
    if img.width > max_width or img.height > max_height:
        width, height = img.size
        while True:
            width -= 1
            height = img.height * width // img.width
            if width <= max_width and height <= max_height:
                break
        img = img.resize((width, height), Image.LANCZOS)
    return img

def image_resize_helper(imageconfig: Dict, img: Image) -> Image:
    img = expand_image_helper(img, imageconfig["minimum_width"], imageconfig["minimum_height"])
    img = shrink_image_helper(img, imageconfig["maximum_width"], imageconfig["maximum_height"])
    return img

def default_maximums_helper(img: Image, config: Dict):
    width, height = img.size
    if config["logo"]["maximum_width"] == None:
        config["logo"]["maximum_width"] = width
    if config["logo"]["maximum_height"] == None:
        config["logo"]["maximum_height"] = height
    if config["image_1"]["maximum_width"] == None:
        config["image_1"]["maximum_width"] = width
    if config["image_1"]["maximum_height"] == None:
        config["image_1"]["maximum_height"] = height
    if config["image_1"]["maximum_height"] == None:
        config["image_1"]["maximum_height"] = width
    if config["image_2"]["maximum_width"] == None:
        config["image_2"]["maximum_width"] = height
    return config