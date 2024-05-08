import keras_ocr
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

def inpaint_text(img_path, pipeline):
    img = keras_ocr.tools.read(img_path) 
    prediction_groups = pipeline.recognize([img])
    
    mask = np.zeros(img.shape[:2], dtype="uint8")
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
            thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
    
    # Inpaint using the mask
    inpainted_img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
    return inpainted_img

# Create the keras_ocr pipeline
pipeline = keras_ocr.pipeline.Pipeline()

# Call the inpaint_text function with your image path and pipeline
img_text_removed = inpaint_text('WEB_Image_LOTUS_Purple_yams_mashed_20x500_Khoai_mo_2081481197163044_plid_8636.jpeg', pipeline)

# Show the inpainted image
plt.imshow(img_text_removed)

# Save the inpainted image
cv2.imwrite('removed_image.jpg', cv2.cvtColor(img_text_removed, cv2.COLOR_BGR2RGB))
