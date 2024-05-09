import os
import keras_ocr
import cv2
import math
import numpy as np
from PIL import Image
import keras_ocr
import tensorflow as tf

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
    img = keras_ocr.tools.read(img_path)
    prediction_groups = pipeline.recognize([img])

    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1]
        x2, y2 = box[1][2]
        x3, y3 = box[1][3]
        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
        if y_mid0 > img.shape[0] / 2 and y_mid1 > img.shape[0] / 2:
            thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)

    inpainted_img = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    base_image = Image.fromarray(inpainted_img)

    image_to_insert = Image.open(image_to_insert_path).convert('RGBA')
    image_data = image_to_insert.getdata()
    new_image_data = [(255, 255, 255, 255) if item[3] == 0 else item[:3] + (255,) for item in image_data]
    image_to_insert.putdata(new_image_data)

    target_size = (max_width, max_height) if max_width and max_height else None
    resized_image = tf.image.resize(image_to_insert, target_size, method=tf.image.ResizeMethod.BILINEAR)
    resized_image_pil = Image.fromarray(resized_image.numpy().astype(np.uint8))

    x = (base_image.width - resized_image_pil.width) // 2
    y = 20 * (base_image.height - resized_image_pil.height) // 23
    base_image.paste(resized_image_pil, (x, y), resized_image_pil)
    
    base_image.save(output_image_path)

def inpaint_and_insert_batch(image_files, input_folder_path, pipeline, image_to_insert_path, output_folder_path, max_width=None, max_height=None):
    for image_file in image_files:
        img_path = os.path.join(input_folder_path, image_file)
        output_image_path = os.path.join(output_folder_path, f'output_{image_file}')
        inpaint_and_insert(img_path, pipeline, image_to_insert_path, output_image_path, max_width, max_height)

#Iterate through each image file in the input folder
for image_file in image_files:
    # Construct the full path to the input image file
    img_path = os.path.join(input_folder_path, image_file)
    
    # Define the paths for output and the image to insert
    image_to_insert_path = 'image001.png'  # Path to the image you want to insert
    output_image_path = os.path.join(output_folder_path, f'output_{image_file}')  # Output image path
    
    # Set the maximum width and height if needed
    max_width = 500
    max_height = 800
    
    # Call the inpaint_and_insert function for each image
    inpaint_and_insert_batch(img_path, pipeline, image_to_insert_path, output_image_path, max_width, max_height)