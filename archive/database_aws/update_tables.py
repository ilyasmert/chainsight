#############################################################################################
# created by Kıvanç Filizci on 04 Jan 2025                                                  #
# SPRINT-4 : ITEM-X : Optimizing the database_aws                                               #
# issue-X : Update 'weekid' column from varchar to integer and modify relevant values       #
#############################################################################################


import psycopg2
from psycopg2 import OperationalError

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="db-chainsight.cd6k86gwohjc.eu-north-1.rds.amazonaws.com",
            port=5432,
            user="metuCeng",
            password="metu-ceng-chainsight",
            dbname="postgres"
        )
        conn.autocommit = True
        return conn
    except OperationalError as e:
        print(f'OperationalError: {e}')
        return None
    except Exception as e:
        print(f'Unexpected error: {e}')
        return None

def update_week_columns(conn):
    try:
        cur = conn.cursor()

        # List of tables and their week columns to be updated
        tables = ['atp_stock', 'intransit', 'ready', 'sales', 'to_be_produced']
        week_column = 'weekid'  # Assuming the column name is 'week'

        for table in tables:
            # Update week values to remove 'W' prefix and convert to integer
            cur.execute(f"""
                UPDATE {table}
                SET {week_column} = CAST(SUBSTRING({week_column} FROM 2) AS INTEGER)
                WHERE {week_column} LIKE 'W%';
            """)

            # Alter the column type to integer
            cur.execute(f"""
                ALTER TABLE {table}
                ALTER COLUMN {week_column} TYPE INTEGER USING {week_column}::integer;
            """)

        print("Week columns updated successfully.")

        # Close the cursor
        cur.close()

    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        update_week_columns(conn)
        conn.close()