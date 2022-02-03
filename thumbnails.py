import os, locale
from PIL import Image, ImageDraw, ImageFont
import datetime
from datetime import timedelta

locale.setlocale(locale.LC_TIME, "de_DE")
YTWIDTH = 1280
YTHEIGHT = 720

def Thumbnails(data, mainfolder, reuse):
	if not reuse:
		mainfolder = os.path.join(mainfolder, "live")
		print("...Thumbnails werden erstellt")
		resize_pics(mainfolder)
		add_texts(data, mainfolder)
		
		check_size(mainfolder)
		delete_not_needed(os.path.join(mainfolder, "Thumbnails"))


def resize_pics(path):
	path = os.path.join(path, "Thumbnails")
	
	pics = [pic for pic in os.listdir(path) if "Folie" in pic]

	for pic in pics:
		img = Image.open(os.path.join(path, pic))
		width, height = img.size
		if img.size == (YTWIDTH, YTHEIGHT):
			continue

		if width < YTWIDTH or height < YTHEIGHT:
			newsize = scale(img, width, height, 1)

		elif width > YTWIDTH or height > YTHEIGHT:
			newsize = scale(img, width, height, -1)

		#print(newsize)
		img = img.resize(newsize, Image.LANCZOS)


		pos1 = (img.width - YTWIDTH) / 2
		pos2 = (img.height - YTHEIGHT) / 2
		img = img.crop((pos1,pos2, YTWIDTH+pos1, YTHEIGHT+pos2))

		img.save(os.path.join(path, pic), quality=95)

def add_texts(data, mainfolder):
	path = os.path.join(mainfolder, "Thumbnails")

	pics = [pic for pic in os.listdir(path) if "Folie" in pic]

	#Bild1
	img = Image.open(os.path.join(path, pics[0]))
	img = box_one(img, mainfolder)

	date = datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M")
	date = date.strftime("%d. %B %H:%M Uhr")

	img = box_two(img, ["Herzliche Einladung!", data["type"] + " am", date])
	img.save(os.path.join(path, pics[0]), quality=95)

	#Bild2
	img = Image.open(os.path.join(path, pics[1]))
	img = box_one(img, mainfolder)

	minute = timedelta(minutes=15)
	date = datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M")
	date = date - minute
	date = date.strftime("%H:%M Uhr")

	img = box_two(img, ["LIVE!\naus der Gemeinde\nab " + date])
	img.save(os.path.join(path, pics[1]), quality=95)

	#Bild3
	img = Image.open(os.path.join(path, pics[2]))
	img = box_one(img, mainfolder)

	date = datetime.datetime.strptime(data['nextdate'], "%Y-%m-%d %H:%M")
	date = date.strftime("%d. %B %H:%M Uhr")

	img = box_two(img, ["Herzliche Einladung!", data["type"] + " am", date])
	img.save(os.path.join(path, pics[2]), quality=95)

#Obere Box
def box_one(img, path):
	#Rechteck
	drawing = ImageDraw.Draw(img)
	drawing.rounded_rectangle([(-20, 20), (540, 140)], radius=15, fill="#FFFFFF", outline=None, width=1)
	#Logo
	logo = Image.open(os.path.join(path, "Thumbnails", "logo.png"))
	img.paste(logo, (20, 33))
	
	#Überschrift1
	font = ImageFont.truetype("calibrib.ttf", 28)
	drawing.text((130, 33), "Gemeinde Hamburg-Alstertal", font=font, fill="#000000")
	#Überschrift2
	font = ImageFont.truetype("calibrib.ttf", 28)
	drawing.text((130, 78), "Neuapostolische Kirche", font=font, fill="#000000")
	#Unterschrift
	font = ImageFont.truetype("calibri.ttf", 28)
	drawing.text((130, 106), "Nord- und Ostdeutschland", font=font, fill="#000000")

	return img

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

def scale(img, width, height, step):
    #print(f"Ausgangswert: {img.size}")
    forrange = YTWIDTH if img.width < YTWIDTH else img.width
    
    for i in range(forrange + 10):
        width += step
        height = img.height * width // img.width
        if step < 0:
            if width <= (YTWIDTH +step) or height <= (YTHEIGHT +step):
                return width, height
        else:
            if width >= YTWIDTH and height >= YTHEIGHT:
                return width, height

def delete_not_needed(path):
	os.remove(os.path.join(path, "calibri.ttf"))
	os.remove(os.path.join(path, "calibrib.ttf"))
	os.remove(os.path.join(path, "logo.png"))