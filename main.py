import os
from thumbnailcreation import ThumbnailCreation
import thumbnailcreation.templates as templates

def main():
	picpath = os.path.join("examples", "clouds.jpg")
	dst = os.path.join("examples", "output.png")
	template = templates.classicBoxTemplate()
	thumbnail = ThumbnailCreation(picpath, dst, template)
	config = thumbnail.template.config
	# Logo
	config["logo"]["activate"] = False # Activate the section
	config["logo"]["logopath"] = os.path.join("examples", "logo.jpg")

	# Section 1
	config["section_1"]["activate"] = False
	#
	# Other lines can be accessed by line2_text and line3_text.

	# Section 2
	config["section_2"]["activate"] = True
	config["section_2"]["line1_text"] = "Eddy is turning one!"
	config["section_2"]["line2_text"] = "We have cakes"
	config["section_2"]["line3_text"] = "Really awesome cupcakes"
	# Also the other lines accessed by line1_text and line2_text.
	
	config["image_1"]["activate"] = True
	config["image_1"]["imagepath"] = os.path.join("examples", "eddy.jpg")
	config["image_2"]["activate"] = True
	config["image_2"]["imagepath"] = os.path.join("examples", "cakes.jpg")
	config["image_2"]["maximum_height"] = 350
	thumbnail.run(config)


if __name__ == "__main__":
	main()
	