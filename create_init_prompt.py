import os
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

api_key = os.environ['OPENAI_API_KEY_V']

# argument "image_path": string
# return "encoded_string": string
def encode_image(image_path):
    # jpg以外は受け付けない
    if not image_path.endswith(".jpg") and not image_path.endswith(".jpeg") and not image_path.endswith(".JPG") and not image_path.endswith(".JPEG"):
        raise Exception("The image must be jpg.")
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
# argument "image_path": string
# return "prompt": string
def create_init_prompt(image_path):
    # 画像のパスがURLの場合はそのまま使う
    image_url = image_path
    # 画像のパスがローカルの場合はbase64にエンコードする
    if not image_path.startswith("http"):
        base64_image = encode_image(image_path)
        image_url = f"data:image/jpeg;base64,{base64_image}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I want to generate this image using DALL-E. Create prompt to input DALL-E. You only need to return the prompt."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        # max_tokensはデフォルト値が結構小さいから指定しないとだめらしい
        "max_tokens": 300,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()

    # print(response.json())
    prompt = response.json().get("choices")[0].get("message").get("content")
    # 両端のクォーテーションマークを削除
    if prompt.startswith('"') and prompt.endswith('"'):
        prompt = prompt[1:-1]
    return prompt

# テスト
prompt = create_init_prompt("data/origin/origin_1.jpg")
print(prompt)