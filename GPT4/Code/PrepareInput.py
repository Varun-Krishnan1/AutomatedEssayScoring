'''
We will present GPT4 with the input as specified in this paper: https://osf.io/2uahv

'''

# Taken from author's paper 
import os

rubric_name = "grammar"
max_score = 5
rubric_description = "Use of syntactic patterns and grammatical accuracy."
num_essays = 294
essays_per_file = 20

prompt = f"I would like you to mark the {rubric_name.lower()} of an essay. Each essay is assigned a rating of 1 to {max_score}, with {max_score} being the highest and 1 the lowest. You don't have to explain why you assign that specific score. Just report a score only. Present the scores as an array ordered from your first essay score to the last. The essay is scored based on the following rubric: {rubric_description}"

essay_files_dir = "../SampleEssays/"
output_dir = "../GPT4_Input/"

for index in range(0, num_essays, essays_per_file):
    file_name = f"{rubric_name}_{index // essays_per_file + 1}.txt"
    file_path = os.path.join(output_dir, file_name)
    essays_in_file = min(essays_per_file, num_essays - index)

    with open(file_path, "w") as file:
        file.write(prompt)

        for essay_index in range(index, index+essays_in_file):
            essay_file_path = os.path.join(essay_files_dir, f"{essay_index}.txt")

            with open(essay_file_path, "r") as essay_file:
                file.write(f"\n\nEssay {essay_index+1}:\n")
                file.write(essay_file.read())

    print(f"Saved essays {index+1} to {index+essays_in_file} in {file_path}")

print("All files saved successfully.")

'''
rubric_name = "grammar" 
max_score = 5
rubric_description = "Use of syntactic patterns and grammatical accuracy."
num_essays = 293

prompt = f"I would like you to mark the {rubric_name.lower()} of an essay. Each essay is assigned a rating of 1 to {max_score}, with {max_score} being the highest and and 1 the lowest.  You don't have to explain why you assign that specific score. Just report a score only. The essay is scored based on the following rubric: {rubric_description}" 

essay_files_dir = "../SampleEssays/"

for index in range(0, num_essays+1):
    file_name = os.path.join(essay_files_dir, f"{index}.txt")
    prompt += f"\n\nEssay {index+1}:\n"
    with open(file_name, "r") as file:
        prompt += file.read()

# print(prompt)

file_path = f"../GPT4_Input/{rubric_name}.txt"  # Replace with the desired file path and name

with open(file_path, "w") as file:
    file.write(prompt)
'''