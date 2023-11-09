import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.environ['OPENAI_API_KEY_V']

# argument "prompt": string
# return "image_url": string
def crete_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
    }
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    # print(response.json())

    image_url = response.json()["data"][0]["url"]
    return image_url


# テスト
prompt = "Photorealistic landscape of a rural scene with a small wooden shack in the foreground, residential houses in the middle distance and a tree-covered hill under a clear blue sky in the background, daytime lighting."
image_url = crete_image(prompt)
print(image_url)