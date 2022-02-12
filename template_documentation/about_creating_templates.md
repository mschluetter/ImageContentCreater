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
This is the required configuration. When somebody wants to create a thumbnail, he/she can config this variables and the thumbnail has to look nice (customer service &#128521;). You can use the variables as you like. Best practice is when the customer wants to use an image or section he/she has to set "activate" to Ture. For images the path has to be added. The maximum sizes will be set later.
## Required methods
You need to implement a constructor and a method named create_thumbnail. The constructor takes no arguments and is needed for the config extension.
```python
# Example: classicBoxTemplate
class classicBoxTemplate(Template):
	def __init__(self):
		self.config["section_1"]["boxcolor"] = "#FFFFFF"
		self.config["section_1"]["boxside"] = "left"
		self.config["section_1"]["line1_color"]= "#000000"
        # continues....
```
The create_thumbnail method is called in the ThumbnailCreation Class. It takes the image where the thumbnail is made of and the configdata (after the customer customised it).
```python
# thumbnailcreation.py -> ThumbnailCreation class:
def add_overlays(self, data: Dict) -> None:
		""" Sets the values for the chosen template"""
		img = Image.open(self.picpath)
		img = self.template.create_thumbnail(img, data)
		
		img.save(self.destination, quality=100)
```
We use the image 
WEITER MACHEN!
# Creating a new template file
First you create a new file in the templates folder. In this case we create the file <strong>classicBoxTemplate.py</strong>. A new template has to inherit from the Template Interface. We have to implement the __init__ method and the create_thumbnail method.
```python
from .templateInterface import Template

class classicBoxTemplate(Template):
    def __init__(self):
        
```