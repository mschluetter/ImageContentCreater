from heapq import merge
import os
import locale
from typing import Dict
from PIL import Image, ImageDraw, ImageFont
import templates

locale.setlocale(locale.LC_TIME, "de_DE")

class ThumbnailCreation:
	YTWIDTH: int = 1280  # Standardwith of Thumbnail
	YTHEIGHT: int = 720  # Standardheight of Thumbnail
	picpath: str
	template: templates.Template

	def __init__(self, picpath, template):
		self.picpath = picpath
		self.template = template

	def run(self, resize_ending=None):
		self.resize_pics(resize_ending)

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
		""" Sets upper box, pic and bottom box"""
		img = Image.open(self.picpath)
		img = self.template.create_thumbnail(img, data)
		
		img.save(self.picpath, quality=100)

	


def Thumbnails(data, mainfolder, reuse):
	if not reuse:
		mainfolder = os.path.join(mainfolder, "live")
		print("...Thumbnails werden erstellt")
		#add_texts(data, mainfolder)
		
		check_size(mainfolder)
		#delete_not_needed(os.path.join(mainfolder, "Thumbnails"))

def check_size(path):
	path = os.path.join(path, "Thumbnails")
	for pic in os.listdir(path):
		temp_path = os.path.join(path, pic)
		quality = 95
		if "Folie" in pic:
			while os.stat(temp_path).st_size > 4000000:
				img = Image.open(pic)
				img.save(path, quality=quality)
				quality -= 5

def delete_not_needed(path):
	os.remove(os.path.join(path, "calibri.ttf"))
	os.remove(os.path.join(path, "calibrib.ttf"))
	os.remove(os.path.join(path, "logo.png"))

def main() -> None:
	thumbnail = ThumbnailCreation("example_low.jpg", templates.classicBoxTemplate())
	thumbnail.resize_pics("png")

	config = thumbnail.template.config
	config["logo"]["activate"] = True
	config["logo"]["logopath"] = os.path.join("examples", "logo_30.jpg")
	config["section_1"]["activate"] = True
	config["section_2"]["activate"] = True
	#config["section_1"]["line1_text"] = "Gemeinde Hamburg-Alstertal"
	config["section_2"]["line1_text"] = "Herzliche Einladung!"
	config["section_2"]["line2_text"] = "Gottesdienst am"
	config["section_2"]["line3_text"] = "03. September um 19:30 Uhr"
	config["image_1"]["activate"] = True
	config["image_1"]["imagepath"] = os.path.join("examples", "example_high.jpg")
	thumbnail.add_overlays(config)

def test():
	pass
 
	
if __name__ == "__main__":
	main()
	#test()

def box_two(img, data):
	height = 200
	width = 620
	laufschrift = 75
	x1 = 1280 - width - 20
	y1 = 720 - height - laufschrift - 20
	x2 = x1 + width + 30
	y2 = y1 + height
	drawing = ImageDraw.Draw(img)
	drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill="#FFFFFF", outline=None, width=1)

	if len(data) == 3:
		font = ImageFont.truetype("calibri.ttf", 45)
		drawing.text((x1 + 17, y1 + 15), data[0], font=font, fill="#000000")
		
		font = ImageFont.truetype("calibrib.ttf", 55)
		drawing.multiline_text((x1 + 17, y1 + 13 + 68), data[1] + "\n" + data[2], font=font, fill="#000000", spacing=15)

		#font = ImageFont.truetype("calibrib.ttf", 55)
		#drawing.text((x1 + 15, y1 + 13 + 58 + 58), data[2], font=font, fill="#000000")

	else:
		lines = data[0].split("\n")
		font = ImageFont.truetype("calibrib.ttf", 55)
		drawing.text((x1 + 17, y1 + 15), lines[0], font=ImageFont.truetype("calibri.ttf", 45), fill="#FF0000")

		drawing.multiline_text((x1 + 17, y1 + 13 + 68), lines[1] + "\n" + lines[2], font=font, fill="#000000", spacing=15)

		#drawing.text((x1 + 15, y1 + 13 + 58 + 58), lines[2], font=font, fill="#000000")
	return img