from PIL import Image, ExifTags
import os
import time
from datetime import datetime
import pathlib

def print_metadata(metadata):
	
	# print non exif metadata
	print("\n-> Image Info:")
	for key, value in metadata.items():
		if key != "exif":
			print(f"{key}: {value}")
	
	# print exif metadata
	if "exif" in metadata:
		print("\n-> EXIF Data:")
		for tag, value in metadata["exif"].items():
			tag_name = ExifTags.TAGS.get(tag, tag)
			print(f"{tag_name}: {value}")
	else:
		print("\n-> No EXIF data available")

		

def get_image_metadata(image_path):
	metadata = {}
	
	try:
		with Image.open(image_path) as img:
			# Get image info
			metadata = img.info
			metadata["Format"] = img.format
			metadata["Mode"] = img.mode
			metadata["Size"] = img.size

			# Get other metadata
			for key, value in metadata.items():
				if key != "exif":
					metadata[key] = value

			# Get EXIF data if available
			exif_data = img.getexif()
			if exif_data:
				metadata["exif"] = exif_data

	except Exception as e:
		print(f"Error retrieving creation date: {e}")

	return metadata

