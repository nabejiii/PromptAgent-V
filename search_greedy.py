from openai import OpenAI
import os
from dotenv import load_dotenv
import csv

from create_init_prompt import create_init_prompt
from improvement import improve_prompt, adjust_prompt_improvement
from image import image_val, create_image, save_image

# from mock import image_val, create_image, save_image, improve_prompt, create_init_prompt

class greedy_search():
    def __init__(self, image_num, dir_name):
        load_dotenv()
        self.image_num = image_num
        self.origin_image = os.path.join("data", "image_" + str(image_num), "origin_" + str(image_num) + ".jpg")
        if not os.path.exists(self.origin_image):
            raise Exception("The image does not exist: " + self.origin_image)
        
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY_V"],
        )
        self.directory = os.path.join("data", "image_" + str(self.image_num), dir_name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        self.diffs = ["none"]
        self.prompts = []
        self.images = []
        self.scores = []
        
        init_prompt = create_init_prompt(self.origin_image)
        self.prompts.append(init_prompt)
        
        init_image_http = create_image(init_prompt)
        init_image = os.path.join(self.directory, "image_" + str(self.image_num) + "_" + str(len(self.images)) + ".jpg")
        save_image(init_image, init_image_http)
        self.images.append(init_image)
        
        init_score = image_val(self.origin_image, init_image)
        self.scores.append(init_score)
        
    def greedy_step(self):
        # generate image
        diff, new_prompt = improve_prompt(self.origin_image, self.images[-1], self.prompts[-1])
        
        new_image_http = create_image(new_prompt)
        new_image = os.path.join(self.directory, "image_" + str(self.image_num) + "_" + str(len(self.images)) + ".jpg")
        save_image(new_image, new_image_http)
        
        new_score = image_val(self.origin_image, new_image)
        
        self.diffs.append(diff)
        self.prompts.append(new_prompt)
        self.images.append(new_image)
        self.scores.append(new_score)

    def greedy_step_with_learning_rate(self, progress):
        # generate image
        diff, new_prompt = adjust_prompt_improvement(self.origin_image, self.images[-1], self.prompts[-1])
        
        new_image_http = create_image(new_prompt)
        new_image = os.path.join(self.directory, "image_" + str(self.image_num) + "_" + str(len(self.images)) + ".jpg")
        save_image(new_image, new_image_http)
        
        new_score = image_val(self.origin_image, new_image)
        
        self.diffs.append(diff)
        self.prompts.append(new_prompt)
        self.images.append(new_image)
        self.scores.append(new_score)
        
    def search(self, max_layer):
        for i in range(max_layer):
            self.greedy_step()
            print("{}/{} steps completed".format(i+1, max_layer))
        self.store_evaluation()

    def search_with_learning_rate(self, max_layer):
        for i in range(max_layer):
            self.greedy_step_with_learning_rate(i / max_layer)
            print("{}/{} steps completed".format(i+1, max_layer))
        self.store_evaluation()

    def store_evaluation(self):
        file_path = os.path.join(self.directory, "evaluation.csv")
        image_id = 0

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Diff", "Prompt", "Image", "Evaluation"])
            for diff, prompt, image, score in zip(self.diffs, self.prompts, self.images, self.scores):
                writer.writerow([image_id, diff, prompt, image, score])
                image_id += 1
                
        print(f"Prompts and evaluations successfully saved to {file_path}")

if __name__ == "__main__":
    greedy = greedy_search(1, "greedy_3")
    greedy.search(10)