from checkers import *
import urllib.request
import re
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import time

def scrape(url, depth_level, save_path):
	
	pages_and_images = extract_links_and_images_from_url(url)

	# print extacted links
	for element in pages_and_images:
		tag_type, element_url = element
		print(tag_type, element_url)
	
	#print extracted images
	""" for element in pages_and_images:
		tag_type, element_url = element
		if tag_type == 'Image':
			print(tag_type, element_url) """
	


	# Recursively scrape urls and download images
	for element in pages_and_images:
		tag_type, element_url = element
		if tag_type == 'Link' and depth_level > 1:
			scrape(element_url, depth_level - 1, save_path)
		if tag_type == 'Image':
			print(tag_type, element_url)
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

def extract_links_and_images_from_url(url):
	response = requests.get(url)
	extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
	
	ordered_elements = []

	# Check if the request was successful
	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')

		print('----------------------')

		print(soup.prettify())

		# print all images
		for element in soup.find_all('img'):
			print(element)
		
		print('----------------------')

		for element in soup.find_all(['a', 'img']):
			if element.name == 'a' and 'href' in element.attrs:
				# Check if the link starts with 'http'
				if element['href'].startswith('http'):
					ordered_elements.append(('Link', element.attrs['href']))
				else:
					ordered_elements.append(('Link', url + element.attrs['href']))
			# Check if the image's src attribute ends with one of the extensions
			elif element.name == 'img':
				src = extract_src(element)
				print(src)
				if src and src.lower().endswith(extensions):
					ordered_elements.append(('Image', src))
	else:
		print(f"An error occurred while fetching the URL: {url}")

	return ordered_elements

def extract_src(element):
	# Check if the element has a src attribute
	if 'src' in element.attrs:
		return element.attrs['src']
	# Check if the element has a data-src attribute
	elif 'data-src' in element.attrs:
		return element.attrs['data-src']
	# Check if the element has a data-lazy attribute
	elif 'data-lazy' in element.attrs:
		return element.attrs['data-lazy']
	# Check if the element has a data-original attribute
	elif 'data-original' in element.attrs:
		return element.attrs['data-original']
	# Check if the element has a data-hi-res-src attribute
	elif 'data-hi-res-src' in element.attrs:
		return element.attrs['data-hi-res-src']
	# Check if the element has a data-hi-res-src attribute
	elif 'data-srcset' in element.attrs:
		return element.attrs['data-srcset']
	return None
	

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
		print ('Downloading image:', url_or_data)
		# Image is represented by a URL
		if url_or_data.startswith('http'):
			url_or_data = remove_query(url_or_data)
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
			image_name = f'{timestamp}_{url_or_data.split("/")[-1]}'

			# Check if the image has an acceptable extension
			if image_has_required_extension(url_or_data):
				save_path = os.path.join(save_path, image_name)
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