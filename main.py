import os
from thumbnailcreation import ThumbnailCreation

def example() -> None:
	picpath = os.path.join("examples", "example.jpg")
	thumbnail = ThumbnailCreation(picpath, resultname="MYTEST", ending="png")
	config = thumbnail.template.config
	config["logo"]["activate"] = True
	config["logo"]["logopath"] = os.path.join("examples", "logo.jpg")
	config["section_1"]["activate"] = True
	config["section_2"]["activate"] = True
	config["image_1"]["activate"] = True
	config["image_1"]["imagepath"] = os.path.join("examples", "image_1.jpg")
	config["image_2"]["activate"] = True
	config["image_2"]["imagepath"] = os.path.join("examples", "image_2.jpg")
	thumbnail.run(config)

def main():
	example()
	
if __name__ == "__main__":
	main()