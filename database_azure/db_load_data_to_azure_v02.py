###################################################
# Script to update tables on Azure PostgreSQL DB  #
# Created on 17 Mar 2025 by Kıvanç Filizci        #
###################################################

# Import the required libraries
import psycopg2
from psycopg2 import OperationalError
import os
import pandas as pd

####################################################
# Define the connection parameters
host            = "db-chainsight.postgres.database.azure.com"
database        = "db-chainsight"
user            = "metuCeng"
password        = "chainsight-2025"
port            = 5432  # default PostgreSQL port
connection      = None
cursor          = None
####################################################

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)


# Function to load data from Excel to PostgreSQL
def load_data_to_db(excel_file, table_name, columns):
    try:
        # Read data from Excel file
        data = pd.read_excel(excel_file)
        print(data.head())

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            sslmode='require'  # Azure enforces SSL
        )
        cursor = connection.cursor()

        # Insert data into the specified table
        for index, row in data.iterrows():
            values = tuple(row[col] for col in columns)
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            cursor.execute(insert_query, values)

        connection.commit()
        print(f"Data loaded into {table_name} table successfully.")

    except OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Load data into pallet_info table
pallet_info_columns = ['productId', 'palletCapacity', 'palletWeight', 'palletUsed']
load_data_to_db('../dataset/dataset_provided/pallet_info.xlsx', 'pallet_info', pallet_info_columns)

# Load data into critical_products table
critical_products_columns = ['productId', 'isCritical']
load_data_to_db('../dataset/dataset_provided/critical_products.xlsx', 'critical_products', critical_products_columns)