import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

firefox_binary_path = "/snap/bin/firefox"

# Specify the path to the GeckoDriver executable
geckodriver_path = "/snap/bin/geckodriver"

# Configure the Firefox service with the binary path
firefox_service = Service(geckodriver_path, firefox_binary=firefox_binary_path)

# Initialize Firefox WebDriver with the configured service
driver = webdriver.Firefox(service=firefox_service)

# Define the URL of the website
url = "http://www.asianfood.no/"

# Define the folder path to save the images
folder_path = 'images_from_website'
os.makedirs(folder_path, exist_ok=True)

# Configure Selenium options for Firefox
firefox_options = Options()
firefox_options.headless = True  # Run Firefox in headless mode

# Initialize the Firefox webdriver with the specified options
# Open the website in the browser
driver.get(url)

# Wait for some time to ensure all content, including images, is loaded
time.sleep(5)  # Adjust this delay as needed

# Find all image tags on the page
image_tags = driver.find_elements(By.TAG_NAME, 'img')

# Loop through the image tags and save each image to the folder
for img in image_tags:
    try:
        img_url = img.get_attribute('src')
        if img_url and not img_url.endswith('ImageNotFound.gif'):
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(folder_path, img_name)

            # Download and save the image
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Downloaded: {img_url}")
            else:
                print(f"Failed to download: {img_url}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Quit the webdriver
driver.quit()

print("Images extracted and saved successfully!")
