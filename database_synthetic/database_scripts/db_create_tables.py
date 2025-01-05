#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : task-1 : create synthetic database and upload datasets                          #
# function-2 : create tables in the database                                                #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError
import sys
import os

#############################################################################################
# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

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

    # Execute a simple query to check the connection
    cur.execute('SELECT version();')
    db_version = cur.fetchone()

    # Write the database version to output file
    with open('outputs/create_tables_output.txt', 'w') as output_file:
        output_file.write(f'Database version: {db_version}\n')

    # Define table structures in a dictionary
    tables = {
        'ready': '''CREATE TABLE IF NOT EXISTS ready (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'sales': '''CREATE TABLE IF NOT EXISTS sales (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'to_be_produced': '''CREATE TABLE IF NOT EXISTS to_be_produced (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETD DATE NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETD)
        );''',
        'intransit': '''CREATE TABLE IF NOT EXISTS intransit (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETA DATE NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETA)
        );''',
        'atp_stock': '''CREATE TABLE IF NOT EXISTS atp_stock (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'ready_last_week': '''CREATE TABLE IF NOT EXISTS ready_last_week (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'sales_last_week': '''CREATE TABLE IF NOT EXISTS sales_last_week (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'to_be_produced_last_week': '''CREATE TABLE IF NOT EXISTS to_be_produced_last_week (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETD DATE NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETD)
        );''',
        'intransit_last_week': '''CREATE TABLE IF NOT EXISTS intransit_last_week (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETA DATE NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETA)
        );''',
        'atp_stock_last_week': '''CREATE TABLE IF NOT EXISTS atp_stock_last_week (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'transportation_info': '''CREATE TABLE IF NOT EXISTS transportation_info (
            transportationId VARCHAR NOT NULL,
            transportationName VARCHAR NOT NULL,
            transportationCapacity INTEGER NOT NULL,
            transportationCost REAL,
            year INTEGER NOT NULL,
            PRIMARY KEY (transportationId, year)
    );''',
        'transportation_info_archive': '''CREATE TABLE IF NOT EXISTS transportation_info_archive (
            transportationId VARCHAR NOT NULL,
            transportationName VARCHAR NOT NULL,
            transportationCapacity INTEGER NOT NULL,
            transportationCost REAL,
            year INTEGER NOT NULL,
            archiveDate DATE NOT NULL,
            PRIMARY KEY (transportationId, year, archiveDate)
    );'''
    }

    # Function to create tables
    def create_table(table_name, table_query):
        cur.execute(table_query)
        with open('outputs/create_tables_output.txt', 'a') as output_file:
            output_file.write(f"{table_name} table created successfully.\n")

    # Iterate through the dictionary and create tables
    table_count = 0
    for table_name, table_query in tables.items():
        create_table(table_name, table_query)
        table_count += 1

    with open('outputs/create_tables_output.txt', 'a') as output_file:
        output_file.write("____________________________________________\n")
        output_file.write(f"{table_count} tables created successfully.\n")

    # Close the cursor and connection
    cur.close()
    conn.close()

except OperationalError as e:
    with open('outputs/create_tables_output.txt', 'a') as output_file:
        output_file.write(f"Error: {e}\n")
