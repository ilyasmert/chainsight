# created by Kıvanç Filizci on 26 Nov 2024
# SPRINT-2 : ITEM-3 : Analysing the Data for the Project
# the excel files provided by the client are summarized in terms of statistics




import pandas as pd
import os

# Define the directory
input_directory = 'datasets_modified'
output_text_file = 'analyzed_data.txt'
output_excel_file = 'analyze_data.xlsx'

# Initialize a dictionary to hold DataFrames for each file's statistics
stats_dict = {}

# Function to compute statistics for a DataFrame
def compute_statistics(df):
    return df.describe()

# Open the text file for writing
with open(output_text_file, 'w') as txt_file:
    # Iterate over all Excel files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(input_directory, filename)

            # Read the Excel file
            df = pd.read_excel(file_path)

            # Compute statistics
            stats = compute_statistics(df)

            # Write statistics to the text file
            txt_file.write(f"Statistics for {filename}:\n")
            txt_file.write(stats.to_string())
            txt_file.write("\n\n")

            # Add the statistics DataFrame to the dictionary
            stats_dict[filename] = stats

# Save the statistics to an Excel file with each file's statistics in a separate sheet
with pd.ExcelWriter(output_excel_file) as writer:
    for filename, stats in stats_dict.items():
        sheet_name = os.path.splitext(filename)[0]
        stats.to_excel(writer, sheet_name=sheet_name)