####################################################
# Script to connect to Azure PostgreSQL database   #
# Created on 07 Mar 2025 by Kıvanç Filizci         #
####################################################

import psycopg2

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
# Connect to the Azure PostgreSQL database_aws
try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
        sslmode='require'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()

    if result:
        print(f"Connected successfully! Result: {result[0]}")

except psycopg2.Error as e:
    print("Error connecting to Azure PostgreSQL:", e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()