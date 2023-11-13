from openai import OpenAI
import os
from dotenv import load_dotenv
import csv

from create_init_prompt import create_init_prompt
from improvement import improve_prompt
from image import image_val, crete_image, save_image

class search():
    def __init__(self, image_num):
        load_dotenv()
        self.image_num = image_num
        self.origin_image = "data/image/origin_" + str(image_num) + ".jpg"
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY_V"],
        )
        self.prompts = []
        self.images = []
        self.scores = []
        
        init_prompt = create_init_prompt(self.origin_image)
        self.prompts.append(init_prompt)
        init_image = crete_image(init_prompt)
        self.images.append(init_image)
        init_score = image_val(self.origin_image, init_image)
        self.scores.append(init_score)
        
    def greedy_step(self):
        # generate image
        new_prompt = improve_prompt(self.origin_image, self.images[-1], self.prompts[-1])
        new_image = crete_image(new_prompt)
        new_score = image_val(self.origin_image, new_image)
        
        self.prompts.append(new_prompt)
        self.images.append(new_image)
        self.scores.append(new_score)
        
    def search_greedy(self, max_layer):
        for i in range(max_layer):
            self.greedy_step()
        self.store_evaluation(self.image_num, self.prompts, self.images, self.scores)

    def store_evaluation(self, image_num, prompts, images, scores):
        directory = os.path.join("data", "image_" + image_num, "data")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_path = os.path.join(directory, "evaluation.csv")
        
        unique_id = len(os.listdir(directory))

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if unique_id == 0:
                writer.writerow(["ID", "Prompt", "Image", "Evaluation"])
                unique_id += 1
            for prompt, image, score in zip(prompts, images, scores):
                writer.writerow([unique_id, prompt, image, score])
                unique_id += 1

        print(f"Prompts and evaluations successfully saved to {file_path}")