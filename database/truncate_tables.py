#############################################################################################
# created by Kıvanç Filizci on 14 Dec 2024                                                  #
# SPRINT-3 : ITEM-1 : Creating the template database                                        #
# issue-5 : Inserting Data into the Tables in Database                                      #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError
import sys

#############################################################################################
with open('outputs/truncate_tables_output.txt', 'w') as output_file:
    sys.stdout = output_file

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
        # Fetch all table names from the public schema
        cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """)
        table_names = [row[0] for row in cur.fetchall()]
        print("Tables found in the public schema:", table_names)

        total_deleted_rows = 0

        # Iterate over each table and truncate it
        for table_name in table_names:
            # Count rows before truncating
            cur.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cur.fetchone()[0]
            total_deleted_rows += row_count

            # Truncate the table
            truncate_table_query = f"TRUNCATE TABLE {table_name} CASCADE;"
            cur.execute(truncate_table_query)
            print(f"Table '{table_name}' truncated successfully, {row_count} rows deleted")
            print("_____________________________________________________________________\n")

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
    sys.stdout = sys.__stdout__

#############################################################################################