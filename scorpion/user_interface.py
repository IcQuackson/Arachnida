from metadata import *
from checkers import *
from metadata import exif_tags

def print_exif_metadata(attributes):
	print("EXIF Data:")
	if "exif" in attributes:
		exif_data = attributes["exif"]
		for key, value in exif_data.items():
			exif_tag_description = exif_tags.get(key, str(key))
			print(f"  ({key}) {exif_tag_description}: {value}")


def open_modify_exif_menu(file):
	
	while True:
		attributes = get_image_attributes(file)
		if "exif" not in attributes:
			print("No EXIF tags found")
			return
		print("-----------------")
		print("Modify EXIF Menu")
		print("1: Add EXIF Data")
		print("2: Delete EXIF Data")
		print("0: Exit")
		print("-----------------")
		choice = int(input("Enter choice: "))
		try:
			if choice == 0:
				break
			elif choice == 1:
				print_exif_metadata(attributes)
				exif_key = int(input("Enter EXIF key: "))
				exif_value = input("Enter EXIF value: ")
				update_image_exif_data(file, {exif_key: exif_value}, [])
				print_exif_metadata(attributes)
			elif choice == 2:
				print_exif_metadata(attributes)
				exif_key = int(input("Enter EXIF key to delete: "))
				update_image_exif_data(file, {}, [exif_key])
				print_exif_metadata(attributes)
		except ValueError:
			print("Invalid choice")
			continue


def open_main_menu(files):
	
	while True:
		print("-----------------")
		print("Modify Menu")
		print("Choose file to modify:")
		for i, file in enumerate(files):
			print(f"{i+1}: {file}")
		print("0: Exit")
		print("-----------------")
		file_index = int(input("Enter choice: "))
		if file_index == 0:
			break
		file_index -= 1
		try:
			if file_index < 0:
				raise IndexError
			file = files[file_index]
		except IndexError:
			print("Invalid choice")
			continue
		attributes = get_image_attributes(file)
		print_metadata(attributes)
		open_modify_exif_menu(file)
