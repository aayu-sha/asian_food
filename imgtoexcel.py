import openpyxl
from openpyxl.drawing.image import Image as ExcelImage
from PIL import Image as PILImage
import os

# Create a new Excel workbook
wb = openpyxl.Workbook()
sheet = wb.active

# Path to the folder containing the images
folder_path = 'output'

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Initialize row counter
row = 1

# Loop through the files in the folder
for file_name in files:
    # Check if the file is an image (you can add more image extensions if needed)
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        # Load the image using PIL
        img = PILImage.open(os.path.join(folder_path, file_name))
        
        # Resize the image if needed
        img = img.resize((50,50))  # Specify the desired width and height
        
        # Create an ExcelImage object from the PIL image
        excel_img = ExcelImage(img)
        
        # Add the image to the Excel sheet
        sheet.add_image(excel_img, f'A{row}')
        
        # Update the row counter
        row += 1

# Save the Excel workbook
wb.save('images.xlsx')
