import os
import locale
from typing import Dict
from urllib.parse import non_hierarchical
from PIL import Image
import templates

class ThumbnailCreation:
	YTWIDTH: int = 1280  # Standardwith of Thumbnail
	YTHEIGHT: int = 720  # Standardheight of Thumbnail
	YTSIZE: int = 4000000 # Standard filesize for thumbnails
	picpath: str
	template: templates.Template
	
	def __init__(self, picpath, template):
		self.picpath = picpath
		self.template = template

	def run(self, data, resize_ending=None):
		self.resize_pics(resize_ending)
		self.add_overlays(data)
		self.check_size()

	def resize_pics(self, pic_ending=None):
		""" Resizes the pic for the youtube format and aligns it to center if it is too large.
		The new pic is saved as self.picpath with an added 2. Optional you can give an ending
		in the variable picending. In the end self.picpath becomes the new safepath.
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
		picformat = img.format
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
		path = os.path.split(self.picpath)
		ending = path[1].split(".")
		
		if pic_ending:
			ending[1] = pic_ending
		else:
			ending[1] = picformat
		
		savepath = os.path.join(path[0], "1.".join(ending))
		img.save(savepath, quality=100, format=ending[1])
		self.picpath = savepath

	def add_overlays(self, data: Dict) -> None:
		""" Sets the values for the chosen template"""
		img = Image.open(self.picpath)
		img = self.template.create_thumbnail(img, data)
		
		img.save(self.picpath, quality=100)

	def check_size(self) -> None:
		""" Checks the size of the file """
		quality = 95
		while os.stat(self.picpath).st_size > self.YTSIZE:
			img = Image.open(self.picpath)
			img.save(self.picpath, quality=quality)
			quality -= 5
			if quality < 5:
				break

def example() -> None:
	picpath = os.path.join("examples", "example.jpg")
	thumbnail = ThumbnailCreation(picpath, templates.classicBoxTemplate())

	config = thumbnail.template.config
	config["logo"]["activate"] = True
	config["logo"]["logopath"] = os.path.join("examples", "logo.jpg")
	config["section_1"]["activate"] = True
	config["section_2"]["activate"] = True
	config["image_1"]["activate"] = True
	config["image_1"]["imagepath"] = os.path.join("examples", "image_1.jpg")
	config["image_2"]["activate"] = True
	config["image_2"]["imagepath"] = os.path.join("examples", "image_2.jpg")
	thumbnail.run(config, "png")

def main() -> None:
	print("Welcome to thumbnail creation. For an example run the example() function.")
	example()
	
if __name__ == "__main__":
	main()