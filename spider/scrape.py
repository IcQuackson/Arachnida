from checkers import *
import urllib.request
import re
import base64
from datetime import datetime
import time

def scrape(url, depth_level, save_path):
	
	pages_and_images = get_pages_and_images(url)

	#if not url_is_valid(url):
		#return

	# Recursively scrape urls and download images
	for element in pages_and_images:
		tag_type, element_url = element
		if tag_type == 'page' and depth_level > 1:
			scrape(element_url, depth_level - 1, save_path)
		if tag_type == 'image':
			download_image(element_url, save_path)

def get_html_content(url):
	html_content = ''
	protocols = ['https://', 'http://']

	try:
		if url.startswith(('http', 'https')):
			with urllib.request.urlopen(url) as response:
				html_content = response.read().decode('utf-8')
				print('Scraping url: ', url)
		else:
			for protocol in protocols:
				try:
					with urllib.request.urlopen(protocol + url) as response:
						html_content = response.read().decode('utf-8')
						print('Scraping url: ',  protocol + url)
						break
				except Exception as e:
					print(f"An unexpected error occurred: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
	
	return html_content

def get_pages_and_images(url):
	# Fetch HTML content from the URL
	html_content = get_html_content(url)

	if html_content == '':
		print(f'Error: There was an error accessing the link {url}')
		return []

	# Regular expressions for extracting URLs and images
	combined_pattern = r"<(?:a\s+(?:[^>]*?\s+)?href=(\"|\')(.*?)\1|img\s+(?:[^>]*?\s+)?src=(\"|\')(.*?)\3)"

	# Find all matches of both URL and image URL patterns in the HTML content
	matches = re.findall(combined_pattern, html_content)

	# Filter out empty matches and extract the URL and tag type
	# Create a list to store Pages and image URLs
	pages_and_images = []
	for quote1, page, quote2, base64_data in matches:
		page = page.strip()
		if page.startswith(('http', 'https', 'www.')) and page not in pages_and_images:
			pages_and_images.append(("page", page))
		elif page.startswith('//www.') and page[2:] not in pages_and_images:
			pages_and_images.append(("page", page[2:]))
		elif base64_data and ("image", base64_data) not in pages_and_images:
			pages_and_images.append(("image", base64_data))

	return pages_and_images

def remove_query(url):
	# Find the index of the first '?' character
	query_index = url.find('?')

	# If '?' is found, return the substring before it
	if query_index != -1:
		return url[:query_index]
	# If '?' is not found, return the original URL
	else:
		return url

def download_image(url_or_data, save_path):
	try:
		# Image is represented by a URL
		if url_or_data.startswith('http'):
			url_or_data = remove_query(url_or_data)
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
			image_name = f'{timestamp}_{url_or_data.split("/")[-1]}'

			# Check if the image has an acceptable extension
			if image_has_required_extension(url_or_data):
				save_path = os.path.join(save_path, image_name)
				print('Downloading image:', image_name)
				# Set a timeout for URL retrieval
				with urllib.request.urlopen(url_or_data, timeout=3) as response:
					with open(save_path, 'wb') as f:
						f.write(response.read())

		# Image is represented by base64-encoded data
		elif url_or_data.startswith('data'):
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
			extension = extract_extension(url_or_data)
			image_name = f"{timestamp}_image." + extension

			acceptable_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

			# Check if the image has an acceptable extension
			if extension in acceptable_extensions:
				image_data = url_or_data.split(",")[1]
				with open(os.path.join(save_path, image_name), 'wb') as f:
					f.write(base64.b64decode(image_data))
					print('Downloading image:', image_name)

	except Exception as e:
		print(f"Error downloading image: {e}")

def extract_extension(data_uri):
	# Split the data URI string using semicolon as delimiter
	parts = data_uri.split(";")

	# Get the first part of the split string which contains the image type
	image_type = parts[0].split(":")[-1]

	# Extract just the extension from the image type
	extension = image_type.split("/")[-1]

	# Check if there's a plus sign in the extension
	if "+" in extension:
		# Choose the first word before the + sign
		extension = extension.split("+")[0]

	return extension