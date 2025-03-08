####################################################
# Script to create tables on Azure PostgreSQL DB   #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

# Import the required libraries
import psycopg2
from psycopg2 import OperationalError
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

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

####################################################
# Connect to the Azure PostgreSQL database_aws
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

# Simple test query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

# Write the database_aws version to output file
    with open('outputs/create_tables_output.txt', 'w') as output_file:
        output_file.write(f'Database version: {db_version}\n')

# Tables to be created
    tables = {
        # current tables
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

        # archive tables
        'ready_archive': '''CREATE TABLE IF NOT EXISTS ready_archive (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            archiveDate DATE NOT NULL,
            archivedBy VARCHAR NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'sales_archive': '''CREATE TABLE IF NOT EXISTS sales_archive (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            archiveDate DATE NOT NULL,
            archivedBy VARCHAR NOT NULL,
            PRIMARY KEY (productId, weekId, year)
        );''',
        'to_be_produced_archive': '''CREATE TABLE IF NOT EXISTS to_be_produced_archive (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETD DATE NOT NULL,
            archiveDate DATE NOT NULL,
            archivedBy VARCHAR NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETD)
        );''',
        'intransit_archive': '''CREATE TABLE IF NOT EXISTS intransit_archive (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            ETA DATE NOT NULL,
            archiveDate DATE NOT NULL,
            archivedBy VARCHAR NOT NULL,
            PRIMARY KEY (productId, weekId, year, ETA)
        );''',
        'atp_stock_archive': '''CREATE TABLE IF NOT EXISTS atp_stock_archive (
            productId VARCHAR NOT NULL,
            quantity REAL,
            weekId INTEGER NOT NULL,
            year INTEGER NOT NULL,
            archiveDate DATE NOT NULL,
            archivedBy VARCHAR NOT NULL,
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
        );''',
        'pallet_info': '''CREATE TABLE IF NOT EXISTS pallet_info (
            productId VARCHAR NOT NULL,
            palletCapacity REAL,
            palletWeight REAL,
            PRIMARY KEY (productId)
        );''',
        'user_roles': '''CREATE TABLE IF NOT EXISTS user_roles (
        roleId VARCHAR NOT NULL,
        roleName VARCHAR NOT NULL,
        PRIMARY KEY (roleId)
        );''',
        'users': '''CREATE TABLE IF NOT EXISTS users (
        userId VARCHAR NOT NULL,
        roleId VARCHAR NOT NULL,
        userName VARCHAR NOT NULL,
        userPassword VARCHAR NOT NULL,
        userEMail VARCHAR NOT NULL,
        PRIMARY KEY (userId),
        FOREIGN KEY (roleId) REFERENCES user_roles(roleId)
        );'''

    }

    # Function to create tables
    def create_table(table_name, table_query):
        cursor.execute(table_query)
        with open('outputs/create_tables_output.txt', 'a') as output_file:
            output_file.write(f"Table '{table_name}' created successfully.\n")

    # Create tables
    count = 0
    for table_name, table_query in tables.items():
        create_table(table_name, table_query)
        count += 1

    with open('outputs/create_tables_output.txt', 'a') as output_file:
        output_file.write("____________________________________________\n")
        output_file.write(f"{count} tables created successfully.\n")

except OperationalError as e:
    with open('outputs/create_tables_output.txt', 'w') as output_file:
        output_file.write(f"OperationalError: {e}\n")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()