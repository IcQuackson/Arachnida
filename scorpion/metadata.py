from PIL import Image
import os
import time
from PIL.ExifTags import TAGS
from datetime import datetime
import pathlib

# EXIF tags lookup table for translation
exif_tags = {
	271: "Make",
	272: "Model",
    274: "Orientation",
    282: "X Resolution",
    283: "Y Resolution",
	284: "Planar Configuration",
    296: "Resolution Unit",
    305: "Software",
    306: "DateTime",
    34665: "Exif IFD Pointer",
    40961: "Color Space",
    40962: "Image Width",
    40963: "Image Height",
	36867: "Date Time Original",
	36868: "Date Time Digitized",
	33434: "Exposure Time",
	33437: "F-Number",
	34850: "Exposure Program",
	34855: "ISO Speed Ratings",
	37377: "Shutter Speed Value",
	37378: "Aperture Value",
	37383: "Metering Mode",
	37384: "Light Source",
	37385: "Flash",
	37386: "Focal Length",
	37500: "Maker Note",
	37510: "User Comment",
	37520: "Subsec Time",
	37521: "Subsec Time Original",
	37522: "Subsec Time Digitized",
	40960: "Flashpix Version",
	40965: "Interoperability IFD Pointer",
	42016: "Image Unique ID",
	42032: "Camera Owner Name",
	42033: "Body Serial Number",
	42034: "Lens Specification",
	42035: "Lens Make",
	42036: "Lens Model",
	42037: "Lens Serial Number",
	42038: "Gamma",
	42080: "MD File Tag",
	42081: "MD Scale Pixel",
	42082: "MD Color Table",
	50708: "Lens Model",
	50710: "Lens Serial Number",
	50711: "Lens Firmware Version",
	50712: "CPU Type",
	50713: "Lens Type",
	50714: "Lens Min Focal Length",
	50715: "Lens Max Focal Length",
	50716: "Lens Max Aperture At Min Focal",
	50717: "Lens Max Aperture At Max Focal",
	50718: "Lens MCU Version",
	50719: "Lens ID",
	50720: "Flash Model",
	50721: "Internal Serial Number",
	50722: "Dust Removal Data",
	50723: "Crop Left Margin",
	50724: "Crop Right Margin",
	50725: "Crop Top Margin",
	50726: "Crop Bottom Margin",
	50727: "Exposure Mode",
	50728: "Flash Activity",
	50729: "Tone Curve",
	50730: "Sharpness",
	50731: "Color Space",
	50732: "Tone Curve Name",
	50733: "Sharpness Frequency",
	50734: "Sensor Red Level",
	50735: "Sensor Blue Level",
	50736: "White Balance Red",
	50737: "White Balance Blue",
	50738: "Color Temperature",
	50739: "Picture Style",
	50740: "Digital Gain",
	50741: "WB Shift AB",
	50742: "WB Shift GM",
	50743: "Measured RGGB",
	50745: "VRD Offset",
	50746: "Sensor Width",
	50747: "Sensor Height",
	50748: "Sensor Left Border",
	50749: "Sensor Top Border",
	50750: "Sensor Right Border",
	50751: "Sensor Bottom Border"
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

def auto_convert_to_type(exif_data, tag, value):
	try:
		tag_str = TAGS.get(tag)
		# Get the type of the tag
		tag_type = TAGS[tag]

		# Convert the value to the right type
		if tag_type == "Ascii":
			exif_data[tag] = str(value)
		elif tag_type == "Byte":
			exif_data[tag] = int(value)
		elif tag_type == "Short":
			exif_data[tag] = int(value)
		elif tag_type == "Long":
			exif_data[tag] = int(value)
		elif tag_type == "Rational":
			exif_data[tag] = (int(value), 1)
		elif tag_type == "Undefined":
			exif_data[tag] = int(value)
		elif tag_type == "SLong":
			exif_data[tag] = int(value)
		elif tag_type == "SRational":
			exif_data[tag] = (int(value), 1)
	except Exception as e:
		print(f"Error converting tag to type: {e}")

""" This function updates the EXIF data of an image file.
	Parameters: image_path - the path to the image file; type: str
				changes - a dictionary containing the changes to be made to the EXIF data; type: dict
				deletions - a list of EXIF tags to be deleted; type: list
	Returns: None
"""
def update_image_exif_data(image_path, changes, deletions):
	print('Image path: ', image_path)
	print('Changes: ', changes)
	print('Deletions: ', deletions)
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
					# Try to convert to right type
					auto_convert_to_type(exif_data, tag, value)

				# Delete specified EXIF data
				for tag in deletions:
					if tag in exif_data:
						del exif_data[tag]

			print('EXIF: ', exif_data)

			# Set the modified EXIF data back to the image
			img.save(image_path, exif=exif_data)
	except Exception as e:
		print(f"Error updating image exif: {e}")


def get_image_attributes(image_path):
	attributes = {}
	
	try:
		with Image.open(image_path) as img:
			# Get image info
			metadata = img.info
			attributes["file_size"] = img.format
			attributes["mode"] = img.mode
			attributes["size"] = img.size

			for key, value in metadata.items():
				if key != "exif":
					attributes[key] = value

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

