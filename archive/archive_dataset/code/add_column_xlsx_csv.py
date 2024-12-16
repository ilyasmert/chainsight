# created by Kıvanç Filizci on 26 Nov 2024
# SPRINT-2 : ITEM-3 : Analysing the Data for the Project
# this script adds a new column "Year" to all Excel and CSV files in the "datasets_old/datasets_modified" directory
# and renames the "Sheet ID" column to "Week Number" if it exists


import pandas as pd
import os

# Define the directory
input_directory = 'datasets_modified'

# Iterate over all files in the input directory
for filename in os.listdir(input_directory):
    file_path = os.path.join(input_directory, filename)

    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        # Read the Excel file
        df = pd.read_excel(file_path)
    elif filename.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(file_path)
    else:
        continue

    # Add the "Year" column
    df['Year'] = 2024

    # Rename the "Sheet ID" column to "Week Number"
    if 'Sheet ID' in df.columns:
        df.rename(columns={'Sheet ID': 'Week Number'}, inplace=True)

    # Save the modified DataFrame back to the file
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        df.to_excel(file_path, index=False)
    elif filename.endswith('.csv'):
        df.to_csv(file_path, index=False)