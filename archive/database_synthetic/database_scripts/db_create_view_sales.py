#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-2 : Conduct a literature review on heuristic approaches for               #
#                       supply chain problems to support development and documentation      #
# issue-1 : create view and triggers for sales table                                        #
#############################################################################################

#############################################################################################
import psycopg2
from psycopg2 import OperationalError, errors
import os

#############################################################################################
# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

#############################################################################################
# Connect to the PostgreSQL database_aws server using the psycopg2 library
try:
    conn = psycopg2.connect(
        host="db-chainsight-synthetic.cd6k86gwohjc.eu-north-1.rds.amazonaws.com",
        port=5432,
        user="metuCeng",
        password="metu-ceng-chainsight",
        dbname="postgres"  # Ensure you specify the database_aws name
    )

    conn.autocommit = True
    cur = conn.cursor()

    # Set datestyle to handle DD.MM.YYYY format
    cur.execute("SET datestyle = 'ISO, DMY';")

    # Create Materialized View for avgSales per productId with explicit cast
    cur.execute('''
        CREATE MATERIALIZED VIEW IF NOT EXISTS sales_avg AS
        SELECT
            productId,
            ROUND(CAST(AVG(quantity) AS NUMERIC), 4) AS avgSales
        FROM sales
        GROUP BY productId;
    ''')

    # Create Function to Refresh Materialized View
    cur.execute('''
        CREATE OR REPLACE FUNCTION refresh_sales_avg()
        RETURNS TRIGGER AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW sales_avg;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    # Create Trigger to Refresh View After Insert
    cur.execute('''
        CREATE TRIGGER sales_avg_update
        AFTER INSERT OR DELETE ON sales
        FOR EACH STATEMENT
        EXECUTE FUNCTION refresh_sales_avg();
    ''')

    with open('outputs/load_data_output.txt', 'a') as output_file:
        output_file.write("Materialized view 'sales_avg' created successfully and trigger set for updates.\n")

    # Close the cursor and connection
    cur.close()
    conn.close()

except OperationalError as e:
    with open('outputs/load_data_output.txt', 'a') as output_file:
        output_file.write(f"Error: {e}\n")
