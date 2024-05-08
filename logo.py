from PIL import Image

def insert_image_above(base_image_path, image_to_insert_path, output_image_path, max_width=None, max_height=None):
    # Open the base image
    base_image = Image.open(base_image_path)
    
    # Open the image to insert and remove transparent background
    image_to_insert = Image.open(image_to_insert_path)
    image_to_insert = image_to_insert.convert('RGBA')
    image_data = image_to_insert.getdata()
    new_image_data = []
    for item in image_data:
        # Remove transparent pixels by setting alpha channel to 255 (fully opaque)
        if item[3] == 0:
            new_image_data.append((255, 255, 255, 255))  # Replace transparent pixel with white
        else:
            new_image_data.append(item[:3] + (255,))  # Keep non-transparent pixels as is
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
    y =20*(base_image.height - new_height )//23 # Place above the bottom of the base image
    
    # Paste the resized image onto the base image
    base_image.paste(resized_image, (x, y), resized_image)
    
    # Save the output image
    base_image.save(output_image_path)

# Example usage with maximum width and height
base_image_path = 'removed_image.jpg'
image_to_insert_path = 'image001.png'
output_image_path = 'output_image.jpg'
max_width = 800  # Set the maximum width
max_height = 600  # Set the maximum height

insert_image_above(base_image_path, image_to_insert_path, output_image_path, max_width, max_height)
