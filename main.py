import os
from thumbnailcreation import ThumbnailCreation
import thumbnailcreation.templates as templates

def main():
	picpath = os.path.join("examples", "example.jpg")
	dst = os.path.join("examples", "mycoolthumbnail.png")
	template = templates.classicBoxTemplate()
	thumbnail = ThumbnailCreation(picpath, dst, template)
	config = thumbnail.template.config
	# Logo
	config["logo"]["activate"] = True # Activate the section
	config["logo"]["logopath"] = os.path.join("examples", "logo.jpg")

	# Section 1
	config["section_1"]["activate"] = True
	config["section_1"]["line1_text"] = "This is the first Line of the section"
	# Other lines can be accessed by line2_text and line3_text.

	# Section 2
	config["section_2"]["activate"] = True
	config["section_2"]["line3_text"] = "Here we enter the third Line"
	# Also the other lines accessed by line1_text and line2_text.

	config["image_1"]["activate"] = True
	config["image_1"]["imagepath"] = os.path.join("examples", "image_1.jpg")
	config["image_2"]["activate"] = True
	config["image_2"]["imagepath"] = os.path.join("examples", "image_2.jpg")
	thumbnail.run(config)
	
if __name__ == "__main__":
	main()