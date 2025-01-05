#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : task-1 : create synthetic database and upload datasets                          #
# function-1 : check connection                                                             #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError

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
    print(f'Database version: {db_version}')
    # Database version: ('PostgreSQL 16.3 on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-17), 64-bit',)

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