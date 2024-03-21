import sys
import shutil
import os

def parse_args(args):

	arg_values = {
		'recursive': False,
		'level': 5,  # Default level
		'save_path': None,
		'url': None
	}

	if len(args) < 1:
		print("Error: no arguments")
		sys.exit(1)

	# Parse command-line arguments
	i = 0
	while i < len(args):
		if args[i] == '-r':
			arg_values['recursive'] = True
			i += 1
		# Checks if -l is being used together with -r
		elif args[i] == '-l' and arg_values['recursive'] == True:
			i += 1
			if i < len(args):
				try:
					arg_values['level'] = int(args[i])
					i += 1
				except ValueError:
					print("Error: Level argument must be an integer.")
					sys.exit(1)
			else:
				print("Error: Missing level argument after -l.")
				sys.exit(1)
		elif args[i] == '-p':
			i += 1
			if i < len(args):
				arg_values['save_path'] = args[i]
				i += 1
			else:
				print("Error: Missing save path argument after -p.")
				sys.exit(1)
		else:
			# URL argument
			if i == len(args) - 1:
				arg_values['url'] = args[i]
			else:
				print("Error: Unexpected argument:", args[i])
				sys.exit(1)
			i += 1

	if arg_values['url'] == None:
		print("Error: no url specified")
		sys.exit(1)

	if arg_values['save_path'] == None and not create_or_replace_directory("data"):
		sys.exit(1)

	if arg_values['save_path'] == None:
		arg_values['save_path'] = 'data'

	if not save_path_is_valid(arg_values['save_path']):
		print("Error: save path is not valid")
		sys.exit(1)

	if arg_values['level'] < 0:
		print("Depth level is not valid:", arg_values['level'])
		return

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

def args_are_valid(args):
	pass

def url_is_valid(url):
	pass

def depth_level_is_valid(depth_level):
	pass

def element_is_url(element):
	pass

def element_is_image(element):
	pass

def image_has_required_extension(image):
	pass

def save_path_is_valid(path):
	print("PATH:", path)
	return os.path.isdir(path) and os.access(path, os.W_OK)