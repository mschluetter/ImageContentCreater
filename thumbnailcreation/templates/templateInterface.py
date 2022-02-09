from abc import ABC, abstractmethod
from typing import Dict
from PIL import Image

class Template(ABC):
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
			"minimum_width": None,
			"minimum_height": None,
			"maximum_width": None,
			"maximum_height": None,
			},
		"image_1": {
			"activate": False,
			"imagepath": None,
			"minimum_width": None,
			"minimum_height": None,
			"maximum_width": None,
			"maximum_height": None,
			},
		"image_2": {
			"activate": False,
			"imagepath": None,
			"minimum_width": None,
			"minimum_height": None,
			"maximum_width": None,
			"maximum_height": None,
			}
		}
    
    @abstractmethod
    def __init__(self):
        """ Set the template related config variables here """
        
    @abstractmethod
    def create_thumbnail(self, img: Image, data: Dict) -> Image:
        """ You get the Image in PIL Format here. Afterwards you return the image..
        	The data is the modified dict from the customer.
         """