import base64
import imgsim
import numpy as np
import cv2
import requests
import os
from dotenv import load_dotenv
import time
from requests.exceptions import Timeout

load_dotenv()

api_key = os.environ['OPENAI_API_KEY_V']

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

# argument "image_path": string, "image_url": string
def save_image(image_path, image_url):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(image_path, 'wb') as out_file:
        out_file.write(response.content)
    print(f"Image successfully downloaded to {image_path}")

# argument "prompt": string
# return "image_url": string
def create_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "dall-e-2",
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
    }

    while True:
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            print("Retrying in ten seconds...")
            time.sleep(10)
            continue

        # print(response.json())
        image_url = response.json()["data"][0]["url"]
        return image_url
        
# if __name__ == "__main__":
#     # テスト
#     prompt = "High-resolution photograph of a contemporary rural Japanese landscape with a modern wooden shack in the foreground, showing power lines and parked cars, residential houses with recent architectural designs scattered in the middle ground, and lush, tree-covered hills in the background, under a clear blue sky with bright daylight."
#     image_url = create_image(prompt)
#     print(image_url)
