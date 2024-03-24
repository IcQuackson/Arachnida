
import os
import sys

def files_are_unique(files):
	return len(set(files)) == len(files)

def files_are_valid(files):
	acceptable_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

	for file in files:
		if not os.path.isfile(file):
			print(f'Error: File {file} does not exist')
			return False
		if not os.access(file, os.R_OK):
			print(f'Error: File {file} does not have read permission')
			return False
		if not file.lower().endswith(acceptable_extensions):
			print(f'Error: allowed extensions: {acceptable_extensions}')
			return False
	return True