import os
import re
import requests
from dotenv import load_dotenv
import time

from image import encode_image

load_dotenv()

# 環境変数を読み込む

api_key = os.environ['OPENAI_API_KEY_V']

def improve_prompt(origin_image, gen_image, pre_prompt):
    encoded_origin_image = encode_image(origin_image)
    encoded_gen_image = encode_image(gen_image)

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
                        "text": f"The objective is to create the best prompt to generate the first given image in Dalle-3. I generated the second image using Dalle-3 by the prompt {pre_prompt}. First, explain the difference between the two given images. And then, based on the initial prompt and the difference between the generated image and the target image, improve the prompt to generate the first given image in Dalle-3."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encoded_origin_image
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encoded_gen_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Generate with the following style: \"diff:\n<diff>\n\nprompt:\n<new prompt>\"",
                    },
                    {
                        "type": "text",
                        "text": "In the <diff> and <new prompt> sections, output only the contents of the diff and the new prompt.",
                    }
                ]
            }
        ],
        "max_tokens": 1000,
    }

    
    while True:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 429:
            print("Rate limit exceeded. Sleeping for a while and retrying...")
            time.sleep(5)  # 5秒待ってからリトライ
            continue
        
        response.raise_for_status()
        
        diff, prompt = extract_diff_and_prompt(response.json().get("choices")[0].get("message").get("content"))
        # 両端のクォーテーションマークを削除
        if prompt.startswith('"') and prompt.endswith('"'):
            prompt = prompt[1:-1]
        
        return diff, prompt

def extract_diff_and_prompt(text):
    diff_pattern = r'diff:\n(.*?)\n\nprompt:'
    prompt_pattern = r'prompt:\n(.*?)$'

    diff_match = re.search(diff_pattern, text, re.DOTALL)
    prompt_match = re.search(prompt_pattern, text, re.DOTALL)

    diff = diff_match.group(1) if diff_match else None
    prompt = prompt_match.group(1) if prompt_match else None

    return diff, prompt

if __name__ == "__main__":
    pre_prompt = "Photorealistic landscape of a rural scene with a small wooden shack in the foreground, residential houses in the middle distance and a tree-covered hill under a clear blue sky in the background, daytime lighting."
    gen_image = "data/image_1/greedy_3/image_1_3.jpg"
    diff, prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)
    print(diff)
    print("=======================")
    print(prompt)
