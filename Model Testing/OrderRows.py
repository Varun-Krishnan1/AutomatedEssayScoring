# Ensure the row-order is the same for all files allowing for concatenation
import os
import pandas as pd
import re

def uniform_row_order(path, output_folder):
    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    reference_data = None
    for file in files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        df['file_number'] = df['filename'].apply(lambda x: int(re.search(r'(\d+)', x).group(1)))
        df_sorted = df.sort_values('file_number')
        
        if reference_data is None:
            reference_data = list(df_sorted['filename'])
        else:
            assert reference_data == list(df_sorted['filename'])
    
        file_name = os.path.splitext(file)[0]
        output_file_name = file_name + "-ordered.csv"
        output_file_path = os.path.join(output_folder, output_file_name)
        df_sorted.to_csv(output_file_path, index=False, columns=df_sorted.columns[:-1]) # don't save file_number col

path = '../Feature Selection Cheating/SampleEssaysFeaturesTruncCheatingNormalizedFiltered/'
output_folder = "SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/"
uniform_row_order(path, output_folder)