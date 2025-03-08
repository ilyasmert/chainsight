####################################################
# Script to load datasets into Azure PostgreSQL DB #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

# Import the required libraries
import os
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import sys
from datetime import datetime

####################################################
# Define the connection parameters
host = "db-chainsight.postgres.database_aws.azure.com"
database = "db-chainsight"
user = "metuCeng"
password = "chainsight-2025"
port = 5432  # default PostgreSQL port
connection = None
cursor = None
####################################################

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)
# Determine the directory containing the CSV files
csv_directory = '../dataset/dataset_chainsight_no_duplicates'

####################################################

# Convert CSV columns to database_aws columns
column_mappings = {
    'ProductId'             : 'productId',
    'WeekId'                : 'weekId',
    'Year'                  : 'year',
    'Quantity'              : 'quantity',
    'ATP_stock'             : 'quantity',
    'Delivery_amount_sq2'   : 'quantity',
    'readyQty'              : 'quantity',
    'Weekly_sales'          : 'quantity',
    'To_be_produced_sq2'    : 'quantity',
    'Etd'                   : 'ETD',
    'Eta'                   : 'ETA'
}

# Define not-null fields for each table
skipped_rows = []
not_null_fields = {
    'ready'         : ['productId', 'weekId', 'year'],
    'sales'         : ['productId', 'weekId', 'year'],
    'to_be_produced': ['productId', 'weekId', 'year', 'ETD'],
    'intransit'     : ['productId', 'weekId', 'year', 'ETA'],
    'atp_stock'     : ['productId', 'weekId', 'year'],
}

success = True

with open('outputs/load_data_to_tables_output.txt', 'w') as output_file:
    sys.stdout = output_file

    try:
        connection = psycopg2.connect(
        host        = "db-chainsight.postgres.database_aws.azure.com",
        database    = "db-chainsight",
        user        = "metuCeng",
        password    = "chainsight-2025",
        port        = 5432,  # default PostgreSQL port
        sslmode='require'
        )

        if connection is None:
            raise OperationalError("Connection failed")
        else:
            print("Connection established successfully")

        connection.autocommit = True
        cursor = connection.cursor()

        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_directory, filename)
                table_name = os.path.splitext(filename)[0]
                archive_table_name = f"{table_name}_archive"

                print(f"Loading data from '{filename}' into table '{archive_table_name}'")

                df = pd.read_csv(file_path)
                df.rename(columns=column_mappings, inplace=True)

                # Convert weekId from 'W45' to integer 45
                if 'weekId' in df.columns:
                    df['weekId'] = df['weekId'].str.extract(r'(\d+)').astype(int)


                for _, row in df.iterrows():
                    if any(pd.isnull(row[field]) for field in not_null_fields.get(table_name, [])):
                        skipped_rows.append({'table': table_name, 'row': row.to_dict()})
                        continue

                    # If loading into an archive table, add archiveDate and archivedBy
                    row_data = row.to_dict()
                    row_columns = list(row.index)
                    row_values = [f"'{row[col]}'" if pd.notna(row[col]) else 'NULL' for col in row_columns]

                    if archive_table_name.endswith('_archive'):
                        columns = ', '.join(row.index.tolist() + ['archiveDate', 'archivedBy'])
                        values = ', '.join([f"'{row[col]}'" if pd.notna(row[col]) else 'NULL' for col in row.index.tolist()] + ["CURRENT_DATE", f"'{user}'"])
                    else:
                        columns = ', '.join(row.index)
                        values = ', '.join([f"'{value}'" if pd.notna(value) else 'NULL' for value in row])


                    insert_query = f"INSERT INTO {archive_table_name} ({columns}) VALUES ({values});"
                    cursor.execute(insert_query)

                print(f"Data from '{filename}' loaded successfully into table '{archive_table_name}', {len(df) - len(skipped_rows)} rows inserted")

        if skipped_rows:
            skipped_df = pd.DataFrame(skipped_rows)
            skipped_df.to_csv('skipped_rows.csv', index=False)
            print("Skipped rows saved to 'skipped_rows.csv'")

        cursor.close()
        connection.close()


    except OperationalError as e:
        print(f'OperationalError: {e}')
        success = False
    except Exception as e:
        print(f'Unexpected error: {e}')
        success = False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    sys.stdout = sys.__stdout__
    if success:
        print("Data loaded successfully!")