""" 
This script removes files that have less than 50 words so they are compatible for TAALED to run on 
"""
import os
import shutil


def count_words(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split()
        return len(words)


def check_folder_files(folder_path, remove_folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            num_words = count_words(file_path)
            if num_words < 50:
                print(
                    f"File '{filename}' has less than 50 words. Removing from '{remove_folder_path}'."
                )
                remove_file_path = os.path.join(remove_folder_path, filename)
                if os.path.exists(remove_file_path):
                    os.remove(remove_file_path)


folder_path = "SampleEssays/"  # Specify the path to the folder with .txt files
remove_folder_path = "SampleEssaysTAALED/"  # Specify the path to the folder to remove files from
check_folder_files(folder_path, remove_folder_path)
