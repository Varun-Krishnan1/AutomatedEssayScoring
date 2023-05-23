""" 
This script did not help in changing the encodings 
"""

import chardet
import os

folder_path = "Tool Validation/Input Essays/"
# folder_path = "TestingWithSampleEssays/SampleEssays/"

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    print(filename)
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):
        # Read the file contents and detect the current encoding
        with open(file_path, "rb") as file:
            content = file.read()
            detected_encoding = chardet.detect(content)["encoding"]

        # Convert the file to utf-8 encoding
        if detected_encoding:
            content_utf8 = content.decode(detected_encoding).encode("utf-8")

            # Write the converted content back to the file
            with open(file_path, "wb") as file:
                file.write(content_utf8)
