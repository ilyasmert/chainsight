#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3 : ITEM-1 : Creating the template database                                        #
# issue-5 : Inserting Data into the Tables in Database                                      #
#############################################################################################

#############################################################################################
import os
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import sys
#############################################################################################

#############################################################################################
csv_directory = '../dataset/dataset_chainsight_no_duplicates'
skipped_rows = []

# Define the NOT NULL fields for each table
not_null_fields = {
    'atp_stock': ['ProductId', 'WeekId', 'Year'],
    'intransit': ['ProductId', 'WeekId', 'Year'],
    'ready': ['ProductId', 'WeekId', 'Year'],
    'sales': ['ProductId', 'WeekId', 'Year'],
    'to_be_produced': ['ProductId', 'WeekId', 'Year']
}

#############################################################################################
with open('outputs/load_data_to_tables_output.txt', 'w') as output_file:
    sys.stdout = output_file

#############################################################################################
    # Connect to the PostgreSQL database server using the psycopg2 library
    try:
        conn = psycopg2.connect(
            host="db-chainsight.cd6k86gwohjc.eu-north-1.rds.amazonaws.com",
            port=5432,
            user="metuCeng",
            password="metu-ceng-chainsight",
            dbname="postgres"  # Ensure you specify the database name
        )

        conn.autocommit = True
        cur = conn.cursor()

#############################################################################################
        # Iterate over all CSV files in the directory
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_directory, filename)
                table_name = os.path.splitext(filename)[0]

                print(f"Loading data from '{filename}' into table '{table_name}'")

                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)

                # Insert the data into the table
                for _, row in df.iterrows():
                    # Check for NULL values in NOT NULL fields
                    if any(pd.isnull(row[field]) for field in not_null_fields.get(table_name, [])):
                        skipped_rows.append({'table': table_name, 'row': row.to_dict()})
                        continue

                    columns = ', '.join(row.index)
                    values = ', '.join([f"'{value}'" if pd.notna(value) else 'NULL' for value in row])
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
                    cur.execute(insert_query)
                print(f"Data from '{filename}' loaded successfully into table '{table_name}', {len(df) - len(skipped_rows)} rows inserted")

        # Save skipped rows to a CSV file
        if skipped_rows:
            skipped_df = pd.DataFrame(skipped_rows)
            skipped_df.to_csv('skipped_rows.csv', index=False)
            print("Skipped rows saved to 'skipped_rows.csv'")

#############################################################################################
        # Close the cursor and connection
        cur.close()
        conn.close()

#############################################################################################
    except OperationalError as e:
        print(f'OperationalError: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

#############################################################################################
    sys.stdout = sys.__stdout__
    print("Data loaded successfully!")