####################################################
# Script to drop tables into Azure PostgreSQL DB   #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

# Import the required libraries
import psycopg2
from psycopg2 import OperationalError
import sys
import os

####################################################
# Define the connection parameters
host = "db-chainsight.postgres.database.azure.com"
database = "db-chainsight"
user = "metuCeng"
password = "chainsight-2025"
port = 5432  # default PostgreSQL port
connection = None
cursor = None
####################################################


####################################################
# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)
success = True

with open('outputs/drop_tables_output.txt', 'w') as output_file:
    sys.stdout = output_file

    connection, cursor = None, None

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

        # Fetch all table names from the public schema
        cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """)
        table_names = [row[0] for row in cursor.fetchall()]

        print("Tables found in the public schema:", table_names)

        for table_name in table_names:
            drop_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
            cursor.execute(drop_table_query)
            print(f"Table '{table_name}' dropped successfully.")

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
        print("Tables dropped successfully!")
