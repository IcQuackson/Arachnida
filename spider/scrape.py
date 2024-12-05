from checkers import *
import urllib.request
import re
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import time

visited = set()

def scrape(url, depth_level, save_path):

	print(f"\033[93mScraping {url} at depth level {depth_level}\033[0m")
	
	pages_and_images = extract_links_and_images_from_url(url)

	# Recursively scrape urls and download images
	for element in pages_and_images:
		tag_type, element_url = element
		if tag_type == 'Link' and depth_level > 1 and element_url not in visited:
			visited.add(element_url)
			scrape(element_url, depth_level - 1, save_path)
		if tag_type == 'Image':
			download_image(element_url, save_path)
	
	print(f"\033[93mFinished scraping {url}\033[0m")


def extract_links_and_images_from_url(url):
	try:
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(f"An error occurred while fetching the URL: {e}")
		return []

	extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
	ordered_elements = []

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')

		for element in soup.find_all(['a', 'img']):
			# Handle links
			if element.name == 'a' and 'href' in element.attrs:
				if element['href'].startswith('http'):
					ordered_elements.append(('Link', element.attrs['href']))
				# Handle relative URLs
				elif element['href'].startswith('/'):
					ordered_elements.append(('Link', requests.compat.urljoin(url, element.attrs['href'])))
			# Handle images
			elif element.name == 'img':
				src = extract_src(element)
				if src:
					ordered_elements.append(('Image', src))

	else:
		print(f"An error occurred while fetching the URL: {url}")

	return ordered_elements

"""
Extracts the source URL of an image element
"""
def extract_src(element):
	if 'src' in element.attrs:
		return element.attrs['src']
	elif 'data-src' in element.attrs:
		return element.attrs['data-src']
	elif 'data-lazy' in element.attrs:
		return element.attrs['data-lazy']
	elif 'data-original' in element.attrs:
		return element.attrs['data-original']
	elif 'data-hi-res-src' in element.attrs:
		return element.attrs['data-hi-res-src']
	elif 'data-srcset' in element.attrs:
		return element.attrs['data-srcset']
	return None
	

def remove_query(url):
	query_index = url.find('?')
	if query_index != -1:
		return url[:query_index]
	else:
		return url

def download_image(img_src, save_path):
	try:
		# Handle image represented by a URL
		if img_src.startswith('http'):
			img_src = remove_query(img_src)
			image_name = add_timestamp_to_image_name(img_src.split("/")[-1])

			# Check if the image has an acceptable extension
			if image_has_required_extension(img_src):
				save_path = os.path.join(save_path, image_name)
				download_image_data_from_url(img_src, save_path)

		# Handle image represented by a Data URI
		elif img_src.startswith('data'):
			extension = extract_extension_from_data_uri(img_src)
			image_name = add_timestamp_to_image_name(f"image.{extension}")

			if is_extension_valid(extension):
				image_data = img_src.split(",")[1] # Extract the base64-encoded image data
				with open(os.path.join(save_path, image_name), 'wb') as f:
					f.write(base64.b64decode(image_data))
					print(f"\033[92mDownloaded image: {image_name}\033[0m")

	except Exception as e:
		print(f"Error downloading image: {e}")

def download_image_data_from_url(url, save_path):
	try:
		urllib.request.urlretrieve(url, save_path)
		print(f"\033[92mDownloaded image: {url}\033[0m")
	except Exception as e:
		print(f"\033[91mError downloading image {url}: {e}\033[0m")

"""
Extracts the extension of an image from a data URI
Example data URI: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABh0lEQVR42mNkAAJqQn+P
"""
def extract_extension_from_data_uri(data_uri):
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

def add_timestamp_to_image_name(image_name):
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
	return f"{timestamp}_{image_name}"