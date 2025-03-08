####################################################
# Script to archive tables on Azure PostgreSQL DB  #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

# Import the required libraries
import pandas as pd
import psycopg2
import os
import datetime

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
# directory paths
base_directory      = "/database_azure_archive_triggers/"
upload_directory    = os.path.join(base_directory, "test_data/week53/")
log_directory       = os.path.join(base_directory, "log_files/")
log_file            = os.path.join(log_directory, "archive_ready_log.txt")

# Ensure output directory exists
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)

####################################################
# possible excel files as input
excel_files = [os.path.join(upload_directory, "ready.xlsx"), os.path.join(upload_directory, "hazır.xlsx")]
csv_file    = os.path.join(upload_directory, "ready.csv")

####################################################
# logged-in user information (to be updated after completion of frontend)
logged_in_user = "systemUser"

####################################################
# function to log messages with a timestamp, table name, and creates log directory if needed
def log_message(message, table_name="ready"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [TABLE: {table_name}] {message}\n"
    with open(log_file, "a") as log_into_file:
        log_into_file.write(log_entry)
    print(log_entry.strip())

####################################################
# function that checks for the existence of 'ready.xlsx' or 'hazır.xlsx' and returns the valid file
def find_excel_file():
    for file in excel_files:
        if os.path.exists(file):
            log_message(f"Found file: {file}")
            return file
    log_message("No Excel file found! Ensure 'ready.xlsx' or 'hazır.xlsx' is present.", table_name="file_check")
    raise FileNotFoundError("Neither 'ready.xlsx' nor 'hazır.xlsx' was found in the directory.")

