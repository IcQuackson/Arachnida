import sys
import shutil
import os
import requests

def parse_args(args):

	arg_values = {
		'recursive': False,
		'level': 1,  # Default level
		'save_path': 'data',
		'url': None
	}

	print(args)

	if len(args) < 1:
		raise ValueError("Error: No arguments provided")

	# Parse command-line arguments
	i = 0
	while i < len(args):
		if args[i] == '-r':
			arg_values['recursive'] = True
			arg_values['level'] = 5
			i += 1
		# Checks if -l is being used together with -r
		elif args[i] == '-l' and arg_values['recursive'] == True:
			i += 1
			if i < len(args):
				try:
					arg_values['level'] = int(args[i])
					i += 1
				except ValueError:
					raise ValueError("Error: Invalid level argument after -l.")
			else:
				raise ValueError("Error: Missing level argument after -l.")
		elif args[i] == '-p':
			i += 1
			if i < len(args):
				arg_values['save_path'] = args[i]
				i += 1
			else:
				raise ValueError("Error: Missing path argument after -p.")
		else:
			# URL argument
			if i == len(args) - 1:
				arg_values['url'] = args[i]
			else:
				raise ValueError("Error: Invalid argument.")
			i += 1
			
	if arg_values['level'] < 0:
		raise ValueError("Error: Invalid level argument.")

	if arg_values['url'] == None:
		raise ValueError("Error: No URL provided")

	if not create_or_replace_directory(arg_values['save_path']):
		raise ValueError("Error: Failed to create or replace directory")

	if not save_path_is_valid(arg_values['save_path']):
		raise ValueError("Error: Invalid save path")

	return arg_values

def create_or_replace_directory(directory_name):
	# Get the full path of the directory
	directory_path = os.path.join(os.getcwd(), directory_name)

	# Check if the directory already exists
	if os.path.exists(directory_path):
		# If it exists, remove everything inside it
		try:
			shutil.rmtree(directory_path)
			print(f"Directory '{directory_name}' already exists. Clearing its contents...")
		except OSError as e:
			print(f"Error: Failed to clear contents of directory '{directory_name}': {e}")
			return False

	# Create the directory
	try:
		os.makedirs(directory_path)
		print(f"Directory '{directory_name}' created successfully at {directory_path}")
		return True
	except OSError as e:
		print(f"Error: Failed to create directory '{directory_name}': {e}")
		return False

def url_is_valid(url):
	try:
		response = requests.head(url)
		return response.status_code == 200 or (response.status_code >= 300 and response.status_code < 400)
	except requests.exceptions.RequestException:
		return False


def image_has_required_extension(image_name):
	acceptable_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
	
	return any(image_name.lower().endswith(ext) for ext in acceptable_extensions)

def save_path_is_valid(path):
	return os.path.isdir(path) and os.access(path, os.W_OK)