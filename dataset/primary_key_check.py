#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3  : ITEM-1 : Creating the template database                                       #
# issue-1   : TTransformation of the Datasets Provided by the Client                        #
#############################################################################################
# Before creating the tables, candidates for the primary key columns should be checked.     #
# The primary key columns should be unique and not null.                                    #
# The following script checks the primary key columns in the dataset provided by the client.#
#############################################################################################

import os
import pandas as pd

# Define the absolute or relative path to the directory containing the CSV files
csv_directory = '../dataset/dataset_chainsight'  # Update this path accordingly

# Open a text file to write the output
with open('primary_key_check_output.txt', 'w') as output_file:
    # Iterate over all CSV files in the directory
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            output_file.write(f"Checking file '{filename}'...\n")

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            output_file.write(f"Columns: {df.columns}\n")

            # Check if 'ProductId' and 'weekId' columns exist
            if 'ProductId' in df.columns and 'WeekId' in df.columns and 'Year' in df.columns:
                # Check for duplicates in the combination of productID and WeekId columns
                if df.duplicated(subset=['ProductId', 'WeekId', 'Year']).any():
                    output_file.write(f"Warning: Duplicates found in file '{filename}'\n")
                    output_file.write("______________________________________\n\n")
                else:
                    output_file.write(f"No duplicates found in file '{filename}'\n")
                    output_file.write("______________________________________\n\n")
            else:
                output_file.write(f"Warning: 'ProductId', 'WeekId', and/or 'Year' columns not found in file '{filename}'\n")
                output_file.write("______________________________________\n\n")