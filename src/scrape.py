from checkers import *
import urllib.request
import re
import base64
from datetime import datetime

def scrape(url, depth_level, save_path):

	print('Scraping url: ', url)

	if not url_is_valid(url):
		return
	
	pages_and_images = get_pages_and_images(url)

	# Recursively scrape urls and download images
	for element in pages_and_images:
		tag_type, element_url = element
		if tag_type == 'page' and depth_level > 1:
			scrape(element_url, depth_level - 1, save_path)
		if tag_type == 'image':
			download_image(element_url, save_path)

def get_pages_and_images(url):
	# Fetch HTML content from the URL
	try:
		with urllib.request.urlopen(url) as response:
			html_content = response.read().decode('utf-8')
	except Exception as e:
		print(f"An unexpected error occurred: {e}")

	# Regular expressions for extracting URLs and images
	combined_pattern = r"<(?:a\s+(?:[^>]*?\s+)?href=(\"|\')(.*?)\1|img\s+(?:[^>]*?\s+)?src=(\"|\')(.*?)\3)"

	# Find all matches of both URL and image URL patterns in the HTML content
	matches = re.findall(combined_pattern, html_content)

	# Filter out empty matches and extract the URL and tag type
	# Create a list to store Pages and image URLs
	pages_and_images = []
	for quote1, page, quote2, base64_data in matches:
		if page.startswith('http'):
			pages_and_images.append(("page", page))
		elif base64_data and ("image", base64_data) not in pages_and_images:
			pages_and_images.append(("image", base64_data))

	return pages_and_images

def download_image(url_or_data, save_path):
	try:
		# Image is represented by a URL
		if url_or_data.startswith('http'):
			image_name = url_or_data.split('/')[-1]

			# Check if the image has an acceptable extension
			if image_has_required_extension(image_name):
				save_path = os.path.join(save_path, image_name)
				urllib.request.urlretrieve(url_or_data, save_path)
				print('Downloading image: ' + image_name)

		# Image is represented by base64-encoded data
		elif url_or_data.startswith('data'):
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			image_name = f"{timestamp}_image.jpg"

			# Check if the image has an acceptable extension
			if image_has_required_extension(image_name):
				image_data = url_or_data.split(",")[1]
				with open(os.path.join(save_path, image_name), 'wb') as f:
					f.write(base64.b64decode(image_data))
					print('Downloading image: ' + image_name)


	except Exception as e:
		print(f"Error downloading image: {e}")