# created by Kıvanç Filizci on 25 Nov 2024
# SPRINT-2 : ITEM-3 : Analysing the Data for the Project
# the excel files provided by the client is in the form of multiple sheets
# this script reads the excel files and creates a merged dataset

import pandas as pd
import os

# Define the directories
input_directory = 'datasets_raw'
output_directory = 'datasets_modified'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate over all Excel files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(input_directory, filename)
        
        # Read the Excel file
        xls = pd.ExcelFile(file_path)
        
        # Initialize an empty DataFrame to hold the merged data
        merged_df = pd.DataFrame()
        
        # Iterate over each sheet in the Excel file
        for sheet_name in xls.sheet_names:
            sheet_df = pd.read_excel(xls, sheet_name=sheet_name)
            sheet_df['Sheet ID'] = sheet_name  # Add the sheet ID column
            merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)
        
        # Save the merged DataFrame to a new Excel file in the output directory
        output_file_path = os.path.join(output_directory, filename)
        merged_df.to_excel(output_file_path, index=False)