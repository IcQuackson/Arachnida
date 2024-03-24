from PIL import Image
import os
import time
from PIL.ExifTags import TAGS

# EXIF tags lookup table for translation
exif_tags = {
    296: "Resolution Unit",
    34665: "Exif IFD Pointer",
    305: "Software",
    274: "Orientation",
    306: "DateTime",
    282: "X Resolution",
    283: "Y Resolution",
    40961: "Color Space",
    40962: "Image Width",
    40963: "Image Height"
}

def print_metadata(attributes):
	
	print("------------------")
	print("| Image Metadata |")
	print("------------------")
	for key, value in attributes.items():
		if key == "exif":
			print("EXIF Data:")
			for exif_key, exif_value in value.items():
				# Translate numerical EXIF tags into human-readable descriptions
				exif_tag_description = exif_tags.get(exif_key, str(exif_key))
				print(f"  {exif_tag_description}: {exif_value}")
		else:
			print(f"  {key.capitalize()}: {value}")

def update_image_exif_data(image_path, changes, deletions):
	try:
		# Open the image
		with Image.open(image_path) as img:
			# Get existing EXIF data
			exif_data = img.info.get("exif")

			# Convert exif_data from bytes to a mutable dictionary
			if exif_data:
				exif_data = img.getexif()

			print('EXIF: ', exif_data)

			# Update existing EXIF data with changes
			if exif_data:
				for tag, value in changes.items():
					exif_data[tag] = value

				# Delete specified EXIF data
				for tag in deletions:
					if tag in exif_data:
						exif_data.pop(tag, None)

			print('EXIF: ', exif_data)

			# Set the modified EXIF data back to the image
			img.save(image_path, exif=exif_data)
	except Exception as e:
		print(f"Error updating image exif: {e}")

def update_image_non_exif_data(image_path, changes, deletions):
	try:
		# Open the image
		with Image.open(image_path) as img:
			# Get existing metadata
			metadata = img.info

			# Update existing metadata with changes
			for key, value in changes.items():
				metadata[key] = value

			# Delete metadata if corresponding value in 'changes' is empty
			for key, value in deletions.items():
				if key in metadata[key]:
					metadata.pop(key, None)

			# Set the modified metadata back to the image
			img.save(image_path, **metadata)
	except Exception as e:
		print(f"Error updating image metadata: {e}")

def get_image_attributes(image_path):
	attributes = {}
	
	try:
		with Image.open(image_path) as img:
			attributes["file_type"] = img.format
			attributes["width"], attributes["height"] = img.size
			attributes["mode"] = img.mode
			
			# Get EXIF data if available
			exif_data = img._getexif()
			if exif_data:
				attributes["exif"] = exif_data

	# Get creation date
		creation_timestamp = os.path.getctime(image_path)
		creation_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(creation_timestamp))
		attributes["creation_date"] = creation_date
	except Exception as e:
		print(f"Error retrieving creation date: {e}")

	return attributes

