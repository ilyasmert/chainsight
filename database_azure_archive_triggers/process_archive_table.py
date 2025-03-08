import sys
import psycopg2
from database_azure_utils import log_message, connect_to_database, convert_excel_to_csv, archive_table, truncate_table, load_csv_to_table

LOGGED_IN_USER = "system_user"

def process_table(table_name):
    log_message(f"Starting data processing for {table_name}.", table_name=table_name)

    csv_file = convert_excel_to_csv(table_name)

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        archive_table(cursor, table_name, LOGGED_IN_USER)
        truncate_table(cursor, table_name)
        load_csv_to_table(cursor, conn, csv_file, table_name)

        log_message(f"All transactions for {table_name} committed successfully.", table_name=table_name)
    except Exception as e:
        conn.rollback()
        log_message(f"Transaction for {table_name} rolled back due to error: {e}", table_name=table_name)
    finally:
        cursor.close()
        conn.close()
        log_message(f"Database connection closed for {table_name}.", table_name=table_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_table_data.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]
    process_table(table_name)
