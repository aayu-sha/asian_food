import os
import pandas as pd
from PIL import Image
import base64

# Specify the path to the folder containing images
folder_path = 'output'

# Initialize lists to store image names and base64 encoded images
image_names = []
base64_images = []

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Load the image using PIL
        img = Image.open(os.path.join(folder_path, filename))

        # Convert the image to base64 format
        with open(os.path.join(folder_path, filename), "rb") as image_file:
            base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Add image name and base64 encoded image to the lists
        image_names.append(filename)
        base64_images.append(base64_encoded_image)

# Create a Pandas DataFrame with image names and base64 encoded images
data = {'Image Name': image_names, 'Base64 Image': base64_images}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
excel_file_path = 'file.xlsx'
df.to_excel(excel_file_path, index=False)

print('Images saved to Excel file as base64 encoded strings.')
