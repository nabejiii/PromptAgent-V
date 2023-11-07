import os
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

api_key = os.environ['OPENAI_API_KEY_V']

# argument "image_path": string
# return "encoded_string": string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
# argument "image_path": string
# return "prompt": string
def create_init_prompt(image_path):
    base64_image = encode_image(image_path)

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
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        # max_tokensはデフォルト値が結構小さいから指定しないとだめらしい
        "max_tokens": 300,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response.json())
    prompt = response.json().get("choices")[0].get("message").get("content")
    # 両端のクォーテーションマークを削除
    if prompt.startswith('"') and prompt.endswith('"'):
        prompt = prompt[1:-1]
    return prompt

# テスト
prompt = create_init_prompt("data/origin/origin_2.jpg")
print(prompt)