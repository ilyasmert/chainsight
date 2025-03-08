####################################################
# Script to archive tables on Azure PostgreSQL DB  #
# This file includes utility functions             #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

####################################################
# Import the required libraries
import os
import json
import datetime
import pandas as pd
import psycopg2

####################################################
# load necessary configurations
config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

base_directory = config["directories"]["base_dir"]
upload_directory = config["directories"]["upload_dir"]
log_directory = config["directories"]["log_dir"]
database_config = config["database_config"]

# ensure log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "process_log.txt")

####################################################
# function to log messages with a timestamp, table name, and creates log directory if needed
def log_message(message, table_name="general"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [TABLE: {table_name}] {message}\n"
    with open(log_file, "a") as log_into_file:
        log_into_file.write(log_entry)
    print(log_entry.strip())

####################################################
# function to connect to the database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname      = database_config["dbname"],
            user        = database_config["user"],
            password    = database_config["password"],
            host        = database_config["host"],
            port        = database_config["port"]
        )
        log_message("Successfully connected to Azure PostgreSQL.", table_name="database")
        return conn
    except Exception as e:
        log_message(f"Database connection failed: {e}", table_name="database")
        raise

####################################################
# function to adjust/find excel files
def find_excel_file(table_name):
    file_variants = config["file_variants"].get(table_name, [])
    excel_files = [os.path.join(upload_directory, filename) for filename in file_variants]

    for file in excel_files:
        if os.path.exists(file):
            log_message(f"Found file: {file}", table_name=table_name)
            return file
    log_message(f"No Excel file found for {table_name}!", table_name=table_name)
    raise FileNotFoundError(f"Expected files for {table_name} were not found.")

####################################################
# function to read data from an excel file and convert it to a csv file
def convert_excel_to_csv(table_name):
    try:
        excel_file = find_excel_file(table_name)
        csv_file = os.path.join(upload_directory, f"{table_name}.csv")
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file, index=False, header=True)
        log_message(f"Converted {excel_file} to {csv_file}.", table_name=table_name)
        return csv_file
    except Exception as e:
        log_message(f"Error converting Excel to CSV: {e}", table_name=table_name)
        raise

####################################################
# function to archive a table
def archive_table(cursor, table_name, logged_in_user):
    try:
        archive_table_name = f"{table_name}_archive"
        columns = config["column_info"]["default_columns"].copy()

        # Check if table has an extra column
        extra_column = config["column_info"]["extra_columns"].get(table_name)
        if extra_column:
            columns.append(extra_column)

        columns.extend(["archiveDate", "archivedBy"])
        column_list = ", ".join(columns)
        select_list = ", ".join(columns[:-2])  # Exclude archiveDate, archivedBy from SELECT

        query = f"""
                INSERT INTO {archive_table_name} ({column_list})
                SELECT {select_list}, CURRENT_TIMESTAMP, %s
                FROM {table_name};
                """
        cursor.execute(query, (logged_in_user,))
        log_message(f"Archived old data from {table_name} to {archive_table_name}.", table_name=table_name)
    except Exception as e:
        log_message(f"Error archiving data for {table_name}: {e}", table_name=table_name)
        raise

####################################################
# function to truncate a table
def truncate_table(cursor, table_name):
    try:
        cursor.execute(f"TRUNCATE TABLE {table_name};")
        log_message(f"Cleared the {table_name} table.", table_name=table_name)
    except Exception as e:
        log_message(f"Error clearing {table_name} table: {e}", table_name=table_name)
        raise

####################################################
# function to load data from a csv file to a table
def load_csv_to_table(cursor, conn, csv_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        columns = config["column_info"]["default_columns"].copy()
        extra_column = config["column_info"]["extra_columns"].get(table_name)
        if extra_column:
            columns.append(extra_column)

        column_list = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        query = f"""
                INSERT INTO {table_name} ({column_list})
                VALUES ({placeholders});
                """

        for _, row in df.iterrows():
            values = [row[col] for col in columns]
            cursor.execute(query, values)

        conn.commit()
        log_message(f"Loaded data from {csv_file} into {table_name} table.", table_name=table_name)
    except Exception as e:
        log_message(f"Error loading CSV data into {table_name}: {e}", table_name=table_name)
        conn.rollback()
        raise