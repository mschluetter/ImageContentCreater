from ast import List
from operator import truediv
import os, locale
from turtle import down
from typing import Dict
from PIL import Image, ImageDraw, ImageFont
import datetime
from datetime import timedelta

locale.setlocale(locale.LC_TIME, "de_DE")


class ThumbnailCreation:
	YTWIDTH: int = 1280  # Standardwith of Thumbnail
	YTHEIGHT: int = 720  # Standardheight of Thumbnail
	picpath: str
	upper_box_defaults: Dict = {
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
		"logopath": None,
	}

	def __init__(self, picpath):
		self.picpath = picpath

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

	def add_overlays(self, upper_data: Dict, picture_data: Dict, down_data: Dict) -> None:
		""" Sets upper box, pic and bottom box"""
		img = Image.open(self.picpath)
		# Set upper Box
		if upper_data["activate"]:
			img = self.upper_box(img, upper_data)

		# if picture_data["activate"]:
		# 	img = self.add_picture(img, picture_data)

		# if down_data["activate"]:
		# 	img = self.down_box(img, down_data)

		img.save(self.picpath, quality=100)


	# HIER WEITER MACHEN!
	def upper_box(self, img: Image, data: Dict) -> Image:
		""" Draw upper Box with choosen data"""

		line1_font = ImageFont.truetype(data["line1_font"], 28)
		line1_size = line1_font.getsize(data["line1_text"])
		line2_font = ImageFont.truetype(data["line2_font"], 28)
		line2_size = line2_font.getsize(data["line2_text"])
		line3_font = ImageFont.truetype(data["line3_font"], 28)
		line3_size = line3_font.getsize(data["line3_text"])
		max_linelen = max([line1_size[0], line2_size[0], line3_size[0]])

		#Spaces outside the box
		topspace = 20
		middlespace = 20
		borderspace = 20
		
		#margin inside the box
		topmargin = 13
		sidemargin = 20
		bottommargin = 13
		default_content = 94  # Default Content height without margin
		if data["logostatus"]:
			logo = Image.open(data["logopath"])
			logospace = logo.width + 13
			if logo.height > default_content:
				default_content = logo.height
		else: 
			logo = None
			logospace = 0

		rectwidth = max_linelen + topspace + middlespace + logospace
		rectheight = default_content + topmargin + bottommargin

		# Boxposition on left
		if data["boxside"] == "left":
			x1 = 0-borderspace
			y1 = topspace
			x2 = rectwidth
			y2 = topspace + rectheight
			box_border_on_image = x1 + borderspace

		# Boxposition on right
		else:
			x1 = img.width-rectwidth
			y1 = topspace
			x2 = img.width + borderspace
			y2 = topspace + rectheight
			box_border_on_image = x1
			
		#Rectangle
		drawing = ImageDraw.Draw(img)
		drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill=data["boxcolor"], outline=None, width=1)
		#Draw Logo
		if logo:
			logo_x = box_border_on_image + sidemargin
			if logo.height < default_content:
				logo_y = round(topspace + topmargin + (default_content - logo.height) / 2)
			else: logo_y = topspace+topmargin
			img.paste(logo, (logo_x, logo_y))
		
		# Line1
		line_x = box_border_on_image + sidemargin + logospace
		line1_y = y1+topmargin
		drawing.text((line_x, line1_y), data["line1_text"], font=line1_font, fill=data["line1_color"])

		# Line 3
		line3_y = y2 - bottommargin
		drawing.text((line_x, line3_y), data["line3_text"], anchor="ls", font=line3_font, fill=data["line3_color"])

		#drawing.line([(x2, y2-bottommargin), (x1, y2-bottommargin)], fill=128)
		# Line2
		drawing.text((line_x, y2-bottommargin - line1_font.getsize("o")[1]), data["line2_text"], anchor="lb", font=line2_font, fill=data["line2_color"])
		
		return img

	def add_picture(self, img: Image, data: Dict) -> Image:
		return img

	def down_box(self, img: Image, data: Dict) -> Image:
		return img


def Thumbnails(data, mainfolder, reuse):
	if not reuse:
		mainfolder = os.path.join(mainfolder, "live")
		print("...Thumbnails werden erstellt")
		add_texts(data, mainfolder)
		
		check_size(mainfolder)
		#delete_not_needed(os.path.join(mainfolder, "Thumbnails"))




def add_texts(data, mainfolder):
	#
	path = os.path.join(mainfolder, "Thumbnails")
	#
	pics = [pic for pic in os.listdir(path) if "Folie" in pic]

	#Bild1
	img = Image.open(os.path.join(path, pics[0]))
	date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
	date = date.strftime("%d. %B %H:%M Uhr")

	img = box_two(img, ["Herzliche Einladung!", data["type"] + " am", date])
	img.save(os.path.join(path, pics[0]), quality=95)

	#Bild2
	img = Image.open(os.path.join(path, pics[1]))

	minute = timedelta(minutes=15)
	date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
	date = date - minute
	date = date.strftime("%H:%M Uhr")

	img = box_two(img, ["LIVE!\naus der Gemeinde\nab " + date])
	img.save(os.path.join(path, pics[1]), quality=95)

	#Bild3
	img = Image.open(os.path.join(path, pics[2]))

	date = datetime.datetime.strptime(data["nextdate"], "%Y-%m-%d %H:%M")
	date = date.strftime("%d. %B %H:%M Uhr")

	img = box_two(img, ["Herzliche Einladung!", data["type"] + " am", date])
	img.save(os.path.join(path, pics[2]), quality=95)

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
	thumbnail = ThumbnailCreation("example_low.jpg")
	thumbnail.resize_pics("png")

	box1 = thumbnail.upper_box_defaults
	box1["activate"] = True
	box1["logostatus"] = True
	box1["logopath"] = os.path.join("examples", "logo3.jpg")
	box1["line1_font"] = "calibrib"
	box1["line2_font"] = "calibrib"
	box1["line1_text"] = "Gemeinde Hamburg-Alstertal"
	#box1["line2_text"] = "Gemeinde Hamburg-Alstertal"
	#box1["line3_text"] = "Gemeinde Hamburg-Alstertal"
	thumbnail.add_overlays(box1,{},{})

if __name__ == "__main__":
	main()