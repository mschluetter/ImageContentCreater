from typing import Dict
from .templateInterface import Template
from .helpers import help_expand_image, help_shrink_image
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
from datetime import timedelta

class classicBoxTemplate(Template):
	def __init__(self):
		self.config["section_1"]["boxcolor"] = "#FFFFFF"
		self.config["section_1"]["boxside"] = "left"
		self.config["section_1"]["line1_color"]= "#000000"
		self.config["section_1"]["line1_font"]= "calibrib"
		self.config["section_1"]["line2_color"]= "#000000"
		self.config["section_1"]["line2_font"]= "calibri"
		self.config["section_1"]["line3_color"]= "#000000"
		self.config["section_1"]["line3_font"]= "calibrib"
		#Spaces outside the box
		self.config["section_1"]["topspace"] = 20
		self.config["section_1"]["middlespace"] = 20
		self.config["section_1"]["borderspace"] = 20
		#margin inside the box
		self.config["section_1"]["topmargin"] = 13
		self.config["section_1"]["sidemargin"] = 20
		self.config["section_1"]["bottommargin"] = 13
		# minimum width and height
		self.config["section_1"]["default_content_height"] = 94  # Default Content height without margin
		self.config["section_1"]["default_box_width"] = 500
		self.config["section_1"]["logospace"] = 0
		# Logostuff
		self.config["logo"]["minimum_height"] = 94
		self.config["logo"]["maximum_height"] = 150
		# Section 2
		self.config["section_2"]["boxcolor"] = "#FFFFFF"
		self.config["section_2"]["boxside"] = "right"
		self.config["section_2"]["line1_color"]= "#000000"
		self.config["section_2"]["line1_font"]= "calibrib"
		self.config["section_2"]["line2_color"]= "#000000"
		self.config["section_2"]["line2_font"]= "calibri"
		self.config["section_2"]["line3_color"]= "#000000"
		self.config["section_2"]["line3_font"]= "calibrib"
		#Spaces outside the box
		self.config["section_2"]["topspace"] = 20
		self.config["section_2"]["middlespace"] = 20
		self.config["section_2"]["borderspace"] = 20
		self.config["section_2"]["bottomspace"] = 75
		#margin inside the box
		self.config["section_2"]["topmargin"] = 13
		self.config["section_2"]["sidemargin"] = 20
		self.config["section_2"]["bottommargin"] = 13
		# minimum width and height
		self.config["section_2"]["default_content_height"] = 200  # Default Content height without margin
		self.config["section_2"]["default_box_width"] = 640
		
	def create_thumbnail(self, img: Image, data: Dict) -> Image:
		# Set upper Box
		if data["section_1"]["activate"]:
			img = self.upper_box(img, data["section_1"], data["logo"])

		if data["section_2"]["activate"]:
			print("Section2")
			img = self.down_box(img, data["section_2"])
			
			
		return img

	def upper_box(self, img: Image, data: Dict, logodata: Dict) -> Image:
		""" Draw upper Box with choosen data"""

		line1_font = ImageFont.truetype(data["line1_font"], 28)
		line1_size = line1_font.getsize(data["line1_text"])
		line2_font = ImageFont.truetype(data["line2_font"], 28)
		line2_size = line2_font.getsize(data["line2_text"])
		line3_font = ImageFont.truetype(data["line3_font"], 28)
		line3_size = line3_font.getsize(data["line3_text"])
		max_linelen = max([line1_size[0], line2_size[0], line3_size[0]])

		# LogoWork
		if logodata["activate"]:
			logo = Image.open(logodata["logopath"])
			if logo.height < logodata["minimum_height"]:
				logo = help_expand_image(logo, 0, logodata["minimum_height"])
			if logo.height > logodata["maximum_height"]:
				logo = help_shrink_image(logo, 999999, logodata["maximum_height"])
			data["logospace"] = logo.width + 13
			if logo.height > data["default_content_height"]:
				data["default_content_height"] = logo.height
		else: 
			logo = None


		rectwidth = max_linelen + data["topspace"] + data["middlespace"] + data["logospace"]
		if rectwidth < data["default_box_width"]:
			rectwidth = data["default_box_width"]
		rectheight = data["default_content_height"] + data["topmargin"] + data["bottommargin"]

		# Boxposition on left
		if data["boxside"] == "left":
			x1 = 0-data["borderspace"]
			y1 = data["topspace"]
			x2 = rectwidth
			y2 = data["topspace"] + rectheight
			box_border_on_image = x1 + data["borderspace"]

		# Boxposition on right
		else:
			x1 = img.width-rectwidth
			y1 = data["topspace"]
			x2 = img.width + data["borderspace"]
			y2 = data["topspace"] + rectheight
			box_border_on_image = x1
			
		#Rectangle
		drawing = ImageDraw.Draw(img)
		drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill=data["boxcolor"], outline=None, width=1)
		#Draw Logo
		if logo:
			logo_x = box_border_on_image + data["sidemargin"]
			if logo.height < data["default_content_height"]:
				logo_y = round(data["topspace"] + data["topmargin"] + (data["default_content_height"] - logo.height) / 2)
			else: logo_y = data["topspace"] + data["topmargin"]
			img.paste(logo, (logo_x, logo_y))
		
		# Line1
		line_x = box_border_on_image + data["sidemargin"] + data["logospace"]
		line1_y = y1 + data["topmargin"]
		drawing.text((line_x, line1_y), data["line1_text"], font=line1_font, fill=data["line1_color"])

		# Line 3
		line3_y = y2 - data["bottommargin"]
		drawing.text((line_x, line3_y), data["line3_text"], anchor="ls", font=line3_font, fill=data["line3_color"])

		# Line2
		drawing.text((line_x, y2-data["bottommargin"] - line1_font.getsize("o")[1]), data["line2_text"], anchor="lb", font=line2_font, fill=data["line2_color"])
		
		return img

	def down_box(self, img: Image, data: Dict) -> Image:
		""" Draw downer Box with choosen data"""
		line1_font = ImageFont.truetype(data["line1_font"], 45)
		line1_size = line1_font.getsize(data["line1_text"])
		line2_font = ImageFont.truetype(data["line2_font"], 55)
		line2_size = line2_font.getsize(data["line2_text"])
		line3_font = ImageFont.truetype(data["line3_font"], 55)
		line3_size = line3_font.getsize(data["line3_text"])
		max_linelen = max([line1_size[0], line2_size[0], line3_size[0]])

		rectwidth = max_linelen + data["topspace"] + data["middlespace"]
		if rectwidth < data["default_box_width"]:
			rectwidth = data["default_box_width"]
		rectheight = data["default_content_height"] + data["topmargin"] + data["bottommargin"]

		# Boxposition on left
		if data["boxside"] == "left":
			x1 = 0-data["borderspace"]
			y1 = img.height - data["bottomspace"] - rectheight - data["topspace"]
			x2 = rectwidth
			y2 = y1 + rectheight
			box_border_on_image = x1 + data["borderspace"]

		# Boxposition on right
		else:
			x1 = img.width-rectwidth
			y1 = img.height - data["bottomspace"] - rectheight - data["topspace"]
			x2 = img.width + data["borderspace"]
			y2 = y1 + rectheight
			box_border_on_image = x1
			
		#Rectangle
		drawing = ImageDraw.Draw(img)
		drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill=data["boxcolor"], outline=None, width=1)
		
		# Line1
		line_x = box_border_on_image + data["sidemargin"]
		line1_y = y1 + data["topmargin"]
		drawing.text((line_x, line1_y), data["line1_text"], font=line1_font, fill=data["line1_color"])

		# Line 3
		line3_y = y2 - data["bottommargin"]
		drawing.text((line_x, line3_y), data["line3_text"], anchor="ls", font=line3_font, fill=data["line3_color"])

		# Line2
		drawing.text((line_x, y2-data["bottommargin"] - line1_font.getsize("o")[1]), data["line2_text"], anchor="lb", font=line2_font, fill=data["line2_color"])
		
		return img

	def add_picture(self, img: Image, data: Dict) -> Image:
		return img

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

