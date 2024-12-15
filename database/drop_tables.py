#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3 : ITEM-1 : Creating the template database                                        #
# issue-4 : Creating Tables in Database                                                     #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError

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
    # List of tables to drop
    tables = ['users', 'atp_stock', 'intransit', 'ready', 'sales', 'to_be_produced', 'production',]

    # Drop each table
    for table in tables:
        drop_table_query = f"DROP TABLE IF EXISTS {table};"
        cur.execute(drop_table_query)
        print(f"Table '{table}' dropped successfully in PostgreSQL")

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