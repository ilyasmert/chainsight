#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : task-1 : create synthetic database and upload datasets                          #
# function-3 : load datasets into to database                                               #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError, errors
import os
import csv

#############################################################################################
# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)
os.makedirs('outputs/skipped', exist_ok=True)

#############################################################################################
# Connect to the PostgreSQL database server using the psycopg2 library
try:
    conn = psycopg2.connect(
        host="db-chainsight-synthetic.cd6k86gwohjc.eu-north-1.rds.amazonaws.com",
        port=5432,
        user="metuCeng",
        password="metu-ceng-chainsight",
        dbname="postgres"  # Ensure you specify the database name
    )

    conn.autocommit = True
    cur = conn.cursor()

    # Set datestyle to handle DD.MM.YYYY format
    cur.execute("SET datestyle = 'ISO, DMY';")

    # Define the directory containing the data files
    data_dir = '../synthetic_dataset_data'

    # Function to format date fields to ISO format
    def format_date(value):
        try:
            return '-'.join(reversed(value.split('.')))
        except Exception:
            return value

    # Function to load data into a table
    def load_data(table_name, file_path):
        skipped_rows_file = f'outputs/skipped/{table_name}_skipped_rows.csv'
        with open(file_path, 'r') as file, open(skipped_rows_file, 'w', newline='') as skipped_file:
            reader = csv.reader(file)
            writer = csv.writer(skipped_file)
            headers = next(reader)

            # Write headers to skipped rows file
            writer.writerow(headers)

            # Construct insert query
            placeholders = ', '.join(['%s'] * len(headers))
            print("inserting into table: ", table_name)
            query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders});"

            # Insert rows
            row_count = 0
            skipped_count = 0
            for row in reader:
                try:
                    # Format date fields if necessary
                    row = [format_date(value) if 'DATE' in headers[i].upper() else value for i, value in enumerate(row)]
                    cur.execute(query, row)
                    row_count += 1
                except (psycopg2.errors.UniqueViolation, psycopg2.errors.DatatypeMismatch, psycopg2.errors.InvalidDatetimeFormat) as e:
                    writer.writerow(row)
                    skipped_count += 1
            print(f"Data loaded into {table_name} successfully with {row_count} records. {skipped_count} rows skipped.")
        with open('outputs/load_data_output.txt', 'a') as output_file:
            output_file.write(f"Data loaded into {table_name} successfully with {row_count} records. {skipped_count} rows skipped.\n")

    # Iterate through CSV files and load data
    file_count = 0
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            table_name = os.path.splitext(filename)[0]  # Remove .csv extension
            file_path = os.path.join(data_dir, filename)
            load_data(table_name, file_path)
            file_count += 1

    with open('outputs/load_data_output.txt', 'a') as output_file:
        output_file.write(f"{file_count} files loaded successfully.\n")

    # Close the cursor and connection
    cur.close()
    conn.close()

except OperationalError as e:
    with open('outputs/load_data_output.txt', 'a') as output_file:
        output_file.write(f"Error: {e}\n")
