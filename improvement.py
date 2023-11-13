import os
from openai import OpenAI
from dotenv import load_dotenv

from image import encode_image

load_dotenv()

# 環境変数を読み込む
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY_V"],
)

def improve_prompt(origin_image, gen_image, pre_prompt):
    encoded_origin_image = encode_image(origin_image)
    encoded_gen_image = encode_image(gen_image)
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"The objective is to create the best prompt to generate the first given image in Dalle-3. I generated the second image using Dalle-3 by the prompt {pre_prompt}. First, explain the difference between the two given images. And then, based on the initial prompt and the difference between the generated image and the target image, improve the prompt to generate the first given image in Dalle-3."},
                    {
                        "type": "image_url",
                        "image_url": encoded_origin_image,
                    },
                    {
                        "type": "image_url",
                        "image_url": encoded_gen_image,
                    },
                    {
                        "type": "text",
                        "text": "Generate with the following style: \"diff:\n<diff>\n\nprompt:\n<prompt>\"",
                    }
                ],
            }
        ],
        max_tokens=1000,
    )
    
    if response.choices[0].finish_reason != None:
        print("explain_diff error, finish_reason:", response.choices[0].finish_reason)
        exit(1)
    print(response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == "__main__":
    pre_prompt = "Photorealistic landscape of a rural scene with a small wooden shack in the foreground, residential houses in the middle distance and a tree-covered hill under a clear blue sky in the background, daytime lighting."
    gen_image = "gen_1.jpg"
    # explain_diff("data/origin/origin_1.jpg", gen_image, pre_prompt)
    improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)
