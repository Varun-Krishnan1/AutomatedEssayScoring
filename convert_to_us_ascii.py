""" 
* This script converts file from utf8 -> us-ascii 
* Even though the manual fot the SALET tools recommends utf8, GAMET skips over files 
that are seemingly UTF-8 due to unknown characters but when us-ascii removes those 
characters then it is able to process the file 
"""
import os
import chardet


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


# folder_path = "TestingWithSampleEssays/SampleEssays/"
folder_path = "1200EssaysRootFolder/Output/EssaysTXT/"

check_num_folder_encoding(folder_path)

# print(len(os.listdir(folder_path)))
# # Iterate over the files in the folder
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)

#     if os.path.isfile(file_path):
#         print(file_path)
#         # Read the file contents in UTF-8 encoding
#         with codecs.open(file_path, "r", encoding="utf-8") as file:
#             content_utf8 = file.read()

#         # Convert the content to US-ASCII encoding
#         content_usascii = content_utf8.encode("ascii", "ignore").decode("ascii")

#         # Write the converted content back to the file
#         with codecs.open(file_path, "w", encoding="us-ascii") as file:
#             file.write(content_usascii)

# print(len(os.listdir(folder_path)))
