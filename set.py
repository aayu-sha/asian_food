import os
import keras_ocr
import cv2
import math
import numpy as np
from PIL import Image
import keras_ocr

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return (x_mid, y_mid)

# Define the folder containing your images
input_folder_path = 'images_from_website'
output_folder_path = 'output'

# Get a list of all files in the input folder
image_files = [f for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]

# Create the keras_ocr pipeline
pipeline = keras_ocr.pipeline.Pipeline()

def inpaint_and_insert(img_path, pipeline, image_to_insert_path, output_image_path, max_width=None, max_height=None):
    # Read the image using keras_ocr tools
    img = keras_ocr.tools.read(img_path)
    
    # Use the pipeline to recognize text in the image
    prediction_groups = pipeline.recognize([img])
    
    # Create a mask for inpainting
    mask = np.zeros(img.shape[:2], dtype="uint8")
    
    # Iterate over recognized text boxes
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1]
        x2, y2 = box[1][2]
        x3, y3 = box[1][3]
        
        # Calculate midpoints of diagonal corners
        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
        
        # Only inpaint if the text is below the midpoint
        if y_mid0 > img.shape[0] / 2 and y_mid1 > img.shape[0] / 2:
            # Calculate line thickness and define the line
            thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
    
    # Inpaint using the mask
    inpainted_img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    
    # Open the base image
    base_image = Image.fromarray(cv2.cvtColor(inpainted_img, cv2.COLOR_BGR2RGB))
    
    # Open the image to insert and remove transparent background
    image_to_insert = Image.open(image_to_insert_path).convert('RGBA')
    image_data = image_to_insert.getdata()
    new_image_data = [(255, 255, 255, 255) if item[3] == 0 else item[:3] + (255,) for item in image_data]
    image_to_insert.putdata(new_image_data)
    
    # Calculate the resizing ratio based on maximum width or height
    width_ratio, height_ratio = 1, 1
    if max_width is not None and image_to_insert.width > max_width:
        width_ratio = max_width / float(image_to_insert.width)
    if max_height is not None and image_to_insert.height > max_height:
        height_ratio = max_height / float(image_to_insert.height)
    resize_ratio = min(width_ratio, height_ratio)
    
    # Resize the image to insert while maintaining aspect ratio
    new_width = int(image_to_insert.width * resize_ratio)
    new_height = int(image_to_insert.height * resize_ratio)
    resized_image = image_to_insert.resize((new_width, new_height))
    
    # Calculate the position to insert the image
    x = (base_image.width - new_width) // 2  # Center horizontally
    y = (base_image.height - new_height) // 2  # Center vertically
    
    # Paste the resized image onto the base image
    base_image.paste(resized_image, (x, y), resized_image)
    
    # Save the output image
    base_image.save(output_image_path)

# Iterate through each image file in the input folder
for image_file in image_files:
    # Construct the full path to the input image file
    img_path = os.path.join(input_folder_path, image_file)
    
    # Define the paths for output and the image to insert
    image_to_insert_path = 'image001.png'  # Path to the image you want to insert
    output_image_path = os.path.join(output_folder_path, f'output_{image_file}')  # Output image path
    
    # Set the maximum width and height if needed
    max_width = 800
    max_height = 600
    
    # Call the inpaint_and_insert function for each image
    inpaint_and_insert(img_path, pipeline, image_to_insert_path, output_image_path, max_width, max_height)
