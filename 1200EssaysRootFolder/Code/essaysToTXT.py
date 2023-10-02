import pandas as pd
import os
import chardet
import codecs

'''
These 2 functions check number of utf8 files in a folder 

Even though the manual fot the SALET tools recommends utf8, GAMET skips over files 
that are seemingly UTF-8 due to unknown characters but when us-ascii removes those 
characters then it is able to process the file 
'''
def is_utf8_encoded(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        if encoding == "utf-8":
            return True
        else:
            return False


def check_num_folder_encoding(folder_path):
    counter = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_utf8_encoded(file_path):
                print(f"UTF-8 encoded file: {file_path}")
                counter += 1

    print(f"Total utf-8 encoded files: {counter}")

 
'''
Convert files from utf8 to us-ascii encoding so that GAMET can process them
'''
def convert_files_to_ascii(folder_path):
  # 110 did not process with GAMET even though only 65 UTF encoded -> 1274/1274 passed after changing
  print(len(os.listdir(folder_path)))
  # Iterate over the files in the folder
  for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)

      if os.path.isfile(file_path):
          print(file_path)
          # Read the file contents in UTF-8 encoding
          with codecs.open(file_path, "r", encoding="utf-8") as file:
              content_utf8 = file.read()

          # Convert the content to US-ASCII encoding
          content_usascii = content_utf8.encode("ascii", "ignore").decode("ascii")

          # Write the converted content back to the file
          with codecs.open(file_path, "w", encoding="us-ascii") as file:
              file.write(content_usascii)

  print(len(os.listdir(folder_path)))

'''
Save each essay from Candidate Answer Text Column as its own txt file in the output folder
Ensure that you save in UTF-8 encoding so the SALAT tools can not have any problems
''' 
def save_essays_as_txt(essays_df):
    essays_df['Candidate Answer Text'] = essays_df['Candidate Response Response'].astype(str)

    output_folder = base_folder + "Output/EssaysTXT/"

    for index, row in essays_df.iterrows():
        candidate_id = row['Candidate ID']
        essay = row['Candidate Answer Text']
        output_file = output_folder + str(candidate_id) + ".txt"
        with open(output_file, "w", encoding='utf-8') as f:
            print("Writing to..." + output_file)
            f.write(essay)


''' 
Save the marking scores for each essay with row name as filename.txt and columns as marking scores 
''' 
def save_marking_scores(essays_df):
  # Select subset of columns
  label_columns = ['Marking Key 1 Score', 'Marking Key 2 Score', 'Marking Key 3 Score', 'Marking Key 4 Score', 'Marking Key 5 Score']

  # Create new column 'filename'
  essays_df['filename'] = (essays_df.reset_index().index + 1).astype(str) + '.txt'  # Added + 1 to the index

  # Reorder columns
  column_order = ['filename'] + label_columns
  df_reordered = essays_df.reindex(columns=column_order)

  df_reordered.to_csv(base_folder + "Output/1200EssayLabels.csv", index=False)


""" 
This function removes files that have less than 50 words so they are compatible for TAALED to run on 
"""
import os
import shutil


def count_words(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split()
        return len(words)


def remove_from_folder(folder_path, remove_folder_path):
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


save_files_as_txt = False
convert_to_utf8 = False
remove_files_for_taaled = True 

base_folder = os.path.dirname(os.getcwd()) + "/"
print("Base folder: " + base_folder)

if save_files_as_txt:
  # Ensure you read the CSV version of the file since that will read in the right number of rows!

  writing_samples = pd.read_csv(base_folder + "Data/Writing Responses 240823.csv")

  print(writing_samples.shape) 
  print(writing_samples.head())

  save_essays_as_txt(writing_samples)
  save_marking_scores(writing_samples)

essay_txts = base_folder + "Output/EssaysTXT/"
  
if convert_to_utf8:
  folder_path = base_folder + "Output/EssaysTXT/"
  check_num_folder_encoding(essay_txts) # was 65 (now none after converting to ascii which also solved 110 files not processed by GAMET to be processed)
  convert_files_to_ascii(essay_txts) 

# Cuts it down to 482 files...
if remove_files_for_taaled:
  # This folder is a duplicate folder of essaysTXT where the files will get deleted from if they have < 50 words 
  remove_folder_path = base_folder + "Output/UsableEssays/"  
  
  remove_from_folder(essay_txts, remove_folder_path)
