###################################################
# Script to update tables on Azure PostgreSQL DB  #
# Created on 17 Mar 2025 by Kıvanç Filizci        #
###################################################

# Import the required libraries
import psycopg2
from psycopg2 import OperationalError
import os

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

####################################################
# Connect to the Azure PostgreSQL database
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        sslmode='require'  # Azure enforces SSL
    )

    connection.autocommit = True
    cursor = connection.cursor()

    # Add a new column to the pallet_info table
    add_column_query = '''
    ALTER TABLE pallet_info
    ADD COLUMN palletUsed INTEGER CHECK (palletUsed IN (0, 1)) DEFAULT 0;
    '''

    # Execute the query to add the new column
    cursor.execute(add_column_query)

    with open('outputs/update_tables_output.txt', 'a') as output_file:
        output_file.write("Column 'palletUsed' added to 'pallet_info' table successfully.\n")

except OperationalError as e:
    with open('outputs/update_tables_output.txt', 'w') as output_file:
        output_file.write(f"OperationalError: {e}\n")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()