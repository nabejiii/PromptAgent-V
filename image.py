import base64
import imgsim
import numpy as np
import cv2

# argument "image_path": string
# return "image_url": string
def encode_image(image_path):
    if image_path.startswith("http"):
        return image_path
    
    # jpg以外は受け付けない
    if not image_path.endswith(".jpg") and not image_path.endswith(".jpeg") and not image_path.endswith(".JPG") and not image_path.endswith(".JPEG"):
        raise Exception("The image must be jpg.")
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{encoded_string}"
        return image_url
    

# argument "image_path1": string, "image_path2": string
# return "distance": float
def image_val(img_path1, img_path2):
    vtr = imgsim.Vectorizer()

    img0 = cv2.imread(img_path1)
    img1 = cv2.imread(img_path2)

    vec0 = vtr.vectorize(img0)
    vec1 = vtr.vectorize(img1)

    dist = imgsim.distance(vec0, vec1)
    return dist