# created by Kıvanç Filizci on 26 Nov 2024
# tin case of necessity csv files will be utilied instead of excel files
# this script reads the csv files and creates a merged dataset


import pandas as pd
import os

# Define the directory
input_directory = 'datasets/datasets_modified'

# Iterate over all Excel files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(input_directory, filename)

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Define the output CSV file path
        output_file_path = os.path.splitext(file_path)[0] + '.csv'

        # Save the DataFrame to a CSV file
        df.to_csv(output_file_path, index=False)