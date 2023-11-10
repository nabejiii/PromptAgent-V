import os
from openai import OpenAI
from dotenv import load_dotenv

from image import encode_image

load_dotenv()

# 環境変数を読み込む
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY_V"],
)

def explain_diff(origin_image, gen_image, pre_prompt):
    encoded_origin_image = encode_image(origin_image)
    encoded_gen_image = encode_image(gen_image)
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"The objective is to create the best prompt to generate the first given image in Dalle-3. I generated the second image using Dalle-3 by the prompt {pre_prompt}. First, explain the difference between the two given images. Only the difference needs to be returned."},
                    {
                        "type": "image_url",
                        "image_url": encoded_origin_image,
                    },
                    {
                        "type": "image_url",
                        "image_url": encoded_gen_image,
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


def improve_prompt(origin_image, gen_image, pre_prompt):
    encoded_origin_image = encode_image(origin_image)
    encoded_gen_image = encode_image(gen_image)
    
    diff = explain_diff(origin_image, gen_image, pre_prompt)
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"The objective is to create the best prompt to generate the first given image in Dalle-3. I generated the second image using Dalle-3 by the prompt {pre_prompt}. First, explain the difference between the two given images."},
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
                        "text": f"{diff}",
                    },
                    {"type": "text", "text": "Now, improve the prompt to generate the first given image in Dalle-3, based on the initial prompt and the difference between the generated image and the target image. Only the prompt needs to be returned with the following style: \"<prompt>\""},
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
    pre_prompt = "Realistic photograph of a rural Japanese landscape with a single wooden shack in the foreground, traditional residential houses scattered in the middle ground, and a large, tree-covered hill dominating the background, under a bright blue sky with clear daylight."
    gen_image = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-Xtb0SN2sQ7TzezyqKkAKmi47/user-b0BTx2MPgLXIaO6363eZSiC3/img-K0Y0TuSrh7RuYLAsIjgIUjc5.png?st=2023-11-09T04%3A23%3A42Z&se=2023-11-09T06%3A23%3A42Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-09T04%3A12%3A31Z&ske=2023-11-10T04%3A12%3A31Z&sks=b&skv=2021-08-06&sig=CBrewZJr13KrtF%2BNwyY0PQaYrBi7GEs5JkgnteSM/7o%3D"
    # explain_diff("data/origin/origin_1.jpg", gen_image, pre_prompt)
    improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)