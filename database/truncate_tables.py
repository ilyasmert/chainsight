#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3 : ITEM-1 : Creating the template database                                        #
# issue-5 : Inserting Data into the Tables in Database                                      #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError

#############################################################################################
# List of table names to truncate
table_names = ['users', 'atp_stock', 'intransit', 'ready', 'sales', 'to_be_produced', 'production']

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
    total_deleted_rows = 0

    # Iterate over each table and truncate it
    for table_name in table_names:
        # Count rows before truncating
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cur.fetchone()[0]
        total_deleted_rows += row_count

        # Truncate the table
        truncate_table_query = f"TRUNCATE TABLE {table_name};"
        cur.execute(truncate_table_query)
        print(f"Table '{table_name}' truncated successfully in PostgreSQL, {row_count} rows deleted")

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