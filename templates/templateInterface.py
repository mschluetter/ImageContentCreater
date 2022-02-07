from abc import ABC, abstractmethod
from typing import Dict

class templateInterface(ABC):
    defaults: Dict = {
		"activate": False,
		"boxcolor": "#FFFFFF",
		"boxside": "left",
		"line1_color": "#000000",
		"line1_font": "calibri",
		"line1_text": "This is line 1 example",
		"line2_color": "#000000",
		"line2_font": "calibri",
		"line2_text": "This is the example Seccond",
		"line3_color": "#000000",
		"line3_font": "calibri",
		"line3_text": "This is an example",
		"logostatus": False,
		"resize_logo": False,
		"logopath": None,
	}

    @abstractmethod
    def create_thumbnail(self, data: Dict) -> None:
        """ Creates the Thumbnail"""