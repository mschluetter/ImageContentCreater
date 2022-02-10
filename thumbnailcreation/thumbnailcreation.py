import os
from typing import Dict
from PIL import Image
import thumbnailcreation.templates as templates

class ThumbnailCreation:
	YTWIDTH: int = 1280  # Standardwith of Thumbnail
	YTHEIGHT: int = 720  # Standardheight of Thumbnail
	YTSIZE: int = 4000000 # Standard filesize for thumbnails
	picpath: str # path to mainpicture
	template: templates.Template #choosen template - default: classicBoxTemplate
	destination: str # Path to Destination
	
	def __init__(self, picpath, destination=None, template=templates.classicBoxTemplate()):
		""" We need the path to the base image and optional the destination. The PIL module 
			can handle common image formats. 
			At last choose a template. The default is the classicBoxTemplate."""
		self.picpath = picpath
		self.template = template
		self.destination = destination

	def run(self, data):
		""" Quickrun for thumbnail creation """
		self.resize_pics()
		self.add_overlays(data)
		self.check_size()

	def resize_pics(self):
		""" Resizes the pic for the youtube format and aligns it to center if it is too large.
		The pic is safed with the picending given in self.picending
		"""
		def scale(img, step):
			""" Scales the with and height based on the step"""
			width, height = img.size
			while True:
				width += step
				height = img.height*width // img.width
				if step < 0:
					if width <= (self.YTWIDTH-step) or height <= (self.YTHEIGHT-step):
						return width, height
				else:
					if width >= self.YTWIDTH and height >= self.YTHEIGHT:
						return width, height
		
		img = Image.open(self.picpath)
		# Check which side is longer and choose a step (up or down)
		# else Statement if the YTWITH and YTHEIGHT is already good.
		if img.width < self.YTWIDTH or img.height < self.YTHEIGHT:
			newsize = scale(img, 1)
		elif img.width > self.YTWIDTH or img.height > self.YTHEIGHT:
			newsize = scale(img, -1)
		else: newsize = img.size

		# Rezise Image and crop pic in center
		img = img.resize(newsize, Image.LANCZOS)
		pos1 = (img.width - self.YTWIDTH) / 2
		pos2 = (img.height - self.YTHEIGHT) / 2
		img = img.crop((pos1,pos2, self.YTWIDTH+pos1, self.YTHEIGHT+pos2))

		# Build new Path and Safe new Pic, Set self.picpath
		if self.destination == None:
			path = os.path.split(self.picpath)
			filename, suffix = path[1].split(".")
			filename += "1"
		else:
			path = os.path.split(self.destination)
			filename, suffix = path[1].split(".")
		
		self.destination = os.path.join(path[0], filename + "." + suffix)
		img.save(self.destination, quality=100, format=suffix)
		self.picpath = self.destination

	def add_overlays(self, data: Dict) -> None:
		""" Sets the values for the chosen template"""
		img = Image.open(self.picpath)
		img = self.template.create_thumbnail(img, data)
		
		img.save(self.destination, quality=100)

	def check_size(self) -> None:
		""" Checks the size of the file """
		quality = 95
		while os.stat(self.picpath).st_size > self.YTSIZE:
			img = Image.open(self.picpath)
			img.save(self.destination, quality=quality)
			quality -= 5
			if quality < 5:
				break

def main() -> None:
	print("Welcome to thumbnail creation.")
	
if __name__ == "__main__":
	main()