# About Creating Templates
In this document you will learn how templates generally work. First we start with the template Interface and how it has to be implemented. In the end you can implement a new template.
# The Template Interface
The Template Intercafe is an abstact class. When we implement this we have access to the default config Dict. We also have to implement the methods init (constructor) and create_thumbnail.
## Default config
```python
config: Dict = {
		"section_1": {
			"activate": False,
			"line1_text": "This is Section1, Line1",
			"line2_text": "This is Section1, Line2",
			"line3_text": "This is Section1, Line3",
			},
		"section_2": {
			"activate": False,
			"line1_text": "This is Section2, Line1",
			"line2_text": "This is Section2, Line2",
			"line3_text": "This is Section2, Line3",
			},
		"logo": {
			"activate": False,
			"logopath": None,
			"minimum_width": 0,
			"minimum_height": 0,
			"maximum_width": None,
			"maximum_height": None,
			},
		"image_1": {
			"activate": False,
			"imagepath": None,
			"minimum_width": 0,
			"minimum_height": 0,
			"maximum_width": None,
			"maximum_height": None,
			},
		"image_2": {
			"activate": False,
			"imagepath": None,
			"minimum_width": 0,
			"minimum_height": 0,
			"maximum_width": None,
			"maximum_height": None,
			}
		}
```
This is the required configuration. When somebody wants to use a template he/she activates a section or an image and adds the linetexts. For images the path has to be added. This should be enough for a good looking result (customer service &#128521;). You as the designer have to take care about the minimum and maximum size. The maximum sizes will be set later (see "Little Helpers" section).
## Required methods
You need to implement a constructor and a method named create_thumbnail. The constructor takes no arguments and is needed for the config extension. Place all extra config variables here.
```python
# Example: classicBoxTemplate
class classicBoxTemplate(Template):
	def __init__(self):
		self.config["section_1"]["boxcolor"] = "#FFFFFF"
		self.config["section_1"]["boxside"] = "left"
		self.config["section_1"]["line1_color"]= "#000000"
        # continues....
```
The create_thumbnail method is called in the ThumbnailCreation Class. It takes the image where the thumbnail components are placed and the configdata (after the customer customised it).
```python
# thumbnailcreation.py -> ThumbnailCreation class:
def add_overlays(self, data: Dict) -> None:
		""" Sets the values for the chosen template"""
		img = Image.open(self.picpath)
		img = self.template.create_thumbnail(img, data)
		
		img.save(self.destination, quality=100)
```
When the method is called the thumbnail creation has to be made and the image has to be returned at the end.
# Creating a new template
To create a new template you create the file with a choosen name in the templates module. Then you need to import the needed stuff. Feel free to use the following starter Template.
```python
from typing import Dict # I use typehints for better Usage
from .templateInterface import Template
from .helpers import image_resize_helper, default_maximums_helper #We'll get to that later
from PIL import Image, ImageDraw, ImageFont

class classicBoxTemplate(Template):
	def __init__(self):
        pass

    def create_thumbnail(self, img: Image, data: Dict) -> Image:
        pass
```
In the constructor you place the config variables that can be accessed by the customer. The create_thumbnail method is needed to create the thumbnail. You place all sections and return the new image. You are just responsible for the content. Saving the image on the right place is not your task.
# Little Helper Functions
There are some checks to make. For that I implemented some helper functions. You don't need to write everything by yourself. If you have some ideas for helpers, feel free to ask.
## default_maximums_helper
This helper function sets all maximum values to the width and height of the base image (the image where the thumbnail components are placed). It checks if the maximum values are None. If they are it sets the value. The best place to call it is in the create_thumbnail method.
```python
def create_thumbnail(self, img: Image, data: Dict) -> Image:
    self.config = helpers.default_maximum_helper(img, self.config)
```
It is important that all maximum and minimum values are set, before calling the image_resize_helper.
## image_resize_helper
The image_resize_helper expands or shrinks an image what has to be placed on the base image. Sometimes it is nesessary to do this because your design requires an image at a good looking size. It needs the config of this image and the actual image. Here an example for the logo. I have extracted the logodata for that.
```python
logo = Image.open(logodata["logopath"])
logo = image_resize_helper(logodata, logo)
```
That is pretty much it. You can use it on every image that has to be placed.
# Adding the template in the init file
After completing your template you have to add the class at the templates init file. Simply import it and the customer can use it.
```python
from .classicBoxTemplate import classicBoxTemplate
```
Congratulations! Now you are done. If you are really nice you can document the template in the template_documentation. Have fun and enjoy creating templates!