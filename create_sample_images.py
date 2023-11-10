import os
from dotenv import load_dotenv

from image import create_image, save_image, image_val
from improvement import improve_prompt

load_dotenv()

api_key = os.environ['OPENAI_API_KEY_V']


init_prompt = "Photorealistic landscape of a rural scene with a small wooden shack in the foreground, residential houses in the middle distance and a tree-covered hill under a clear blue sky in the background, daytime lighting."

# プロンプト修正
# pre_prompt = init_prompt
# gen_image = "data/samples/init0.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

modified_prompt = "High-resolution photograph of a rural Japanese village scene with a detailed wooden shack in the foreground, various residential houses with distinctive roof tiles in the middle distance, and a lush green hill with dense tree coverage under a vivid blue sky with minimal clouds, natural daylight setting."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(modified_prompt)
#     save_image(f"data/samples/first_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = modified_prompt
# gen_image = "data/samples/first_modified0.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

second_modified_prompt = "High-resolution photograph of a solitary wooden shack with horizontal planks in the foreground of a rural Japanese village, an open grassy field to the left of the shack, no immediate neighboring houses, residential homes with unique tiled roofs in the background, a densely forested hill extending into the distance, against a clear blue sky with minimal clouds, natural daylight setting."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(second_modified_prompt)
#     save_image(f"data/samples/second_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = second_modified_prompt
# gen_image = "data/samples/second_modified1.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

third_modified_prompt = "High-resolution photograph of a wooden shack with visible horizontal planks situated on the right side of the frame in a rural Japanese village, a space on the left with grass and a few parked cars, neighboring homes with distinct tiled roofs visible nearby, a densely wooded hill in the background, under a clear blue sky with a few clouds, natural daylight setting."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(third_modified_prompt)
#     save_image(f"data/samples/third_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = third_modified_prompt
# gen_image = "data/samples/third_modified1.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

fourth_modified_prompt = "High-resolution photograph of a single standalone wooden shack with visible horizontal planks, positioned on the right side of the frame on a grassy field in a rural Japanese village, with no immediate neighboring buildings to its right or left and some distant houses with tiled roofs on the far right, a densely wooded hill dominating the background, under a vast clear blue sky with minimal cloud cover, in a natural daylight setting."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(fourth_modified_prompt)
#     save_image(f"data/samples/fourth_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = fourth_modified_prompt
# gen_image = "data/samples/fourth_modified0.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

fifth_modified_prompt = "High-resolution photograph of a well-maintained, new-looking wooden shack with a simple pitched roof, situated on the right side of the image in an open grassy field within a rural Japanese village setting. No neighboring structures immediately to the right or left, with contemporary homes featuring tiled roofs visible in the far right background. A lush, densely forested mountain spans the entire backdrop. The scene is under a vast, clear blue sky with very few clouds, in bright natural daylight."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(fifth_modified_prompt)
#     save_image(f"data/samples/fifth_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = fifth_modified_prompt
# gen_image = "data/samples/fifth_modified0.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

sixth_modified_prompt = "High-resolution photograph of a simple, modern wooden shack with a sharp pitched roof on the left side of the frame, located in an expansive grassy field within a rural village in Japan. The shack is well-maintained and new-looking, with no adjacent buildings to the immediate right or left, but with contemporary homes having tiled roofs in the background on the far right. The scene includes a vibrant, densely wooded mountain filling the backdrop, under an expansive clear blue sky with minimal cloud cover, captured in bright, natural daylight."
# # 修正後のpromptで2枚生成
# for i in range(2):
#     image_url = create_image(sixth_modified_prompt)
#     save_image(f"data/samples/sixth_modified{i}.jpg", image_url)

# 生成した画像を元にプロンプト修正
# pre_prompt = sixth_modified_prompt
# gen_image = "data/samples/sixth_modified1.jpg"
# modified_prompt = improve_prompt("data/image_1/origin_1.jpg", gen_image, pre_prompt)

seventh_modified_prompt = "High-resolution photograph of a traditional, all-wooden shack with a sharp pitched roof, centrally located in the frame, situated in a grassy clearing by a rural village in Japan, with no adjacent structures to the immediate right or left. The shack features closed double doors and is flanked by mature trees. In the background, to the far right, there are homes with distinctly curved, tiled roofs. A lush, green mountain looms in the backdrop, and the scene is set under a vibrant, clear blue sky with almost no clouds. The picture captures the essence of bright, natural daylight without any visible power lines or electrical poles."
# 修正後のpromptで2枚生成
for i in range(2):
    image_url = create_image(seventh_modified_prompt)
    save_image(f"data/samples/seventh_modified{i}.jpg", image_url)