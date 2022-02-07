from typing import Dict
from .templateInterface import templateInterface

class classicBoxTemplate(templateInterface):
    def create_thumbnail(self, data: Dict) -> None:
        print(self.defaults)