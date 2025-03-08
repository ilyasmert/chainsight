#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3  : ITEM-1 : Creating the template database_aws                                       #
# issue-1   : Transformation of the Datasets Provided by the Client                         #
#############################################################################################
# Dataset provided by the client is in the form of Excel files, containing multiple sheets. #
# The goal is to merge the data from all sheets in each Excel file into a single DataFrame, #
#       add a "Year" column with the current year,                                          #
#       and save the merged data to a new Excel file and a CSV file.                        #
# The modified dataset has column names in English and the following mappings:              #
#       'Product' -> 'ProductId'                                                            #
#       'ATP stock' -> 'ATP_stock'                                                          #
#       'Delivery amount (m2)' -> 'Delivery_amount_sq2'                                     #
#       'hazır' -> 'readyQty'                                                               #
#       'weekly sales' -> 'Weekly_sales'                                                    #
#       'Toplam Üretimde Bekleyen (M2)' -> 'To_be_produced_sq2'                             #
#       'Son TerminTarihi' -> 'Etd'                                                         #
# The modified dataset has additional columns:                                              #
#       'Year' -> the current year                                                          #
#       'WeekId' -> the sheet ID                                                            #
#############################################################################################

#############################################################################################
# import the required libraries
import pandas as pd
import os
from datetime import datetime

#############################################################################################
# Define the directories
input_directory = 'dataset_provided'
output_directory = 'dataset_chainsight_with_duplicates'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get the current year
current_year = datetime.now().year

# Column name mappings
column_mappings = {
    'Product': 'ProductId',
    'ATP stock': 'ATP_stock',
    'Delivery amount (m2)': 'Delivery_amount_sq2',
    'hazır': 'readyQty',
    'weekly sales': 'Weekly_sales',
    'Toplam Üretimde Bekleyen (M2)': 'To_be_produced_sq2',
    'Son TerminTarihi': 'Etd'
}

# Counters for the number of files processed
excel_files_converted = 0
excel_files_created = 0
csv_files_created = 0

# Function to convert Excel files to CSV
def convert_excel_to_csv(file_path):
    df = pd.read_excel(file_path)
    output_file_path = os.path.splitext(file_path)[0] + '.csv'
    df.to_csv(output_file_path, index=False)
    return output_file_path

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
            sheet_df['WeekId'] = sheet_name  # Add the sheet ID column
            merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)

        # Rename columns based on the mappings
        merged_df.rename(columns=column_mappings, inplace=True)

        # Add the "Year" column
        merged_df['Year'] = current_year

        # Save the merged DataFrame to a new Excel file in the output directory
        output_file_path = os.path.join(output_directory, filename)
        merged_df.to_excel(output_file_path, index=False)
        excel_files_created += 1

        # Convert the new Excel file to CSV
        convert_excel_to_csv(output_file_path)
        csv_files_created += 1
        excel_files_converted += 1

#############################################################################################
# Print the number of files processed
print(f'Number of Excel files converted: {excel_files_converted}')
print(f'Number of Excel files created: {excel_files_created}')
print(f'Number of CSV files created: {csv_files_created}')