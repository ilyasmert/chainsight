#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# updated on 16 Dec 2024 accordingly with "no duplicate" modification                       #
# SPRINT-3  : ITEM-1 : Creating the template database                                       #
# issue-1   : Transformation of the Datasets Provided by the Client                         #
#############################################################################################
# Before creating the tables, candidates for the primary key columns should be checked.     #
# The primary key columns should be unique and not null.                                    #
# The following script checks the primary key columns in the dataset provided by the client.#
#############################################################################################


import os
import pandas as pd

# Define the path to the directory containing the CSV files
csv_directory = '../dataset/dataset_chainsight_no_duplicates'  # Updated accordingly for duplicate elimination (16.12.2024)

# Define the primary keys for each table
primary_keys = {
    'atp_stock': ['ProductId', 'WeekId', 'Year'],
    'ready': ['ProductId', 'WeekId', 'Year'],
    'sales': ['ProductId', 'WeekId', 'Year'],
    'intransit': ['ProductId', 'WeekId', 'Year', 'Eta'],
    'to_be_produced': ['ProductId', 'WeekId', 'Year', 'Etd']
}

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

            # Determine the table name from the filename (without extension)
            table_name = os.path.splitext(filename)[0]

            # Check if the table has a defined primary key
            if table_name in primary_keys:
                primary_key = primary_keys[table_name]

                # Check for duplicates in the primary key columns
                if df.duplicated(subset=primary_key).any():
                    output_file.write(f"Warning: Duplicates found in file '{filename}' based on primary key {primary_key}\n")
                    output_file.write("______________________________________\n\n")
                else:
                    output_file.write(f"No duplicates found in file '{filename}' based on primary key {primary_key}\n")
                    output_file.write("______________________________________\n\n")
            else:
                output_file.write(f"Warning: Primary key not defined for table '{table_name}'\n")
                output_file.write("______________________________________\n\n")