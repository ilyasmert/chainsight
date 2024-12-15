#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3 : ITEM-1 : Creating the template database                                        #
# issue-3 : Connecting to the Database Using pgAdmin and Python                             #
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

    # Execute a simple query to check the connection
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    print(f'Database version: {db_version}')
    # Output: Database version: ('PostgreSQL 12.5 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit',)

#############################################################################################

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