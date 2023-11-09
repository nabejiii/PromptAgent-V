import os
import csv

# arguments "image_path": string, "prompt": string, "evaluation": float
def store_evaluations(image_path, prompt, evaluation):
    # Create the directory if it doesn't exist
    directory = os.path.join(image_path, "data")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Create a file to save the prompt and evaluation in CSV format
    file_path = os.path.join(directory, "evaluation.csv")
    
    # Generate a unique ID for each row (you can use a more sophisticated method if needed)
    unique_id = len(os.listdir(directory))  # Count existing files
    
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if unique_id == 0:  # Write header only for the first row
            writer.writerow(["ID", "Prompt", "Evaluation"])
        writer.writerow([unique_id, prompt, evaluation])
    print(f"Prompt and evaluation successfully saved to {file_path}")
