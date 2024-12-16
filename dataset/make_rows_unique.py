#############################################################################################
# created by Kıvanç Filizci on 16 Dec 2024                                                  #
# SPRINT-3  : ITEM-1 : Creating the template database                                       #
# issue-1   : TTransformation of the Datasets Provided by the Client                        #
#############################################################################################
# The datasets provided by the Client include duplicate rows.                               #
# To enhance an effective database, Primary Key constraints should be established.          #
# Therefore a further information exchange was conducted with the Client.                   #
# The Client confirmed that the rows are supposed to be unique in the datasets, and for the #
# datasets that contain duplicate rows, the duplicates should be summed up.                 #
# The following script is developed to make the rows unique in the datasets.                #
#############################################################################################

import os
import pandas as pd
import sys

# Define the directories containing the dataset files and the output directory
dataset_directory = 'dataset_chainsight_with_duplicates'
output_directory = 'dataset_chainsight_no_duplicates'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Define the primary keys for each table
primary_keys = {
    'atp_stock': ['ProductId', 'WeekId', 'Year'],
    'ready': ['ProductId', 'WeekId', 'Year'],
    'sales': ['ProductId', 'WeekId', 'Year'],
    'intransit': ['ProductId', 'WeekId', 'Year', 'Eta'],
    'to_be_produced': ['ProductId', 'WeekId', 'Year', 'Etd']
}

# Function to process a DataFrame and return unique primary key rows
def process_dataframe(df, primary_key):
    initial_rows = len(df)
    grouped_df = df.groupby(primary_key).sum().reset_index()
    final_rows = len(grouped_df)
    duplicate_rows = initial_rows - final_rows
    return grouped_df, initial_rows, duplicate_rows, final_rows

# Redirect standard output to a file
with open('make_rows_unique_output.txt', 'w') as output_file:
    sys.stdout = output_file
    file_index = 1

    # Process Excel files first
    for filename in os.listdir(dataset_directory):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(dataset_directory, filename)

            # Read the file into a DataFrame
            df = pd.read_excel(file_path)

            # Determine the table name from the filename (without extension)
            table_name = os.path.splitext(filename)[0]

            # Check if the table has a defined primary key
            if table_name in primary_keys:
                primary_key = primary_keys[table_name]

                # Process the DataFrame to get unique primary key rows
                unique_df, initial_rows, duplicate_rows, final_rows = process_dataframe(df, primary_key)

                # Save the processed DataFrame to a new file in the output directory
                output_file_path = os.path.join(output_directory, filename)
                unique_df.to_csv(output_file_path, index=False)
                print(f'{file_index}. {filename} processed and saved unique rows to {output_file_path}')
                print(f'\t Initial number of rows: {initial_rows}')
                print(f'\t Number of duplicate rows: {duplicate_rows}')
                print(f'\t Final number of rows: {final_rows}')
                print("______________________________________\n\n")
                file_index += 1

    # Process CSV files next
    for filename in os.listdir(dataset_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(dataset_directory, filename)

            # Read the file into a DataFrame
            df = pd.read_csv(file_path)

            # Determine the table name from the filename (without extension)
            table_name = os.path.splitext(filename)[0]

            # Check if the table has a defined primary key
            if table_name in primary_keys:
                primary_key = primary_keys[table_name]

                # Process the DataFrame to get unique primary key rows
                unique_df, initial_rows, duplicate_rows, final_rows = process_dataframe(df, primary_key)

                # Save the processed DataFrame to a new file in the output directory
                output_file_path = os.path.join(output_directory, filename)
                unique_df.to_csv(output_file_path, index=False)
                print(f'{file_index}. {filename} processed and saved unique rows to {output_file_path}')
                print(f'\t Initial number of rows: {initial_rows}')
                print(f'\t Number of duplicate rows: {duplicate_rows}')
                print(f'\t Final number of rows: {final_rows}')
                print("______________________________________\n\n")
                file_index += 1

    # Reset standard output to default
    sys.stdout = sys.__stdout__