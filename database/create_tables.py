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

    # Execute a simple query to check the connection
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    print(f'Database version: {db_version}')
    # Output: Database version: ('PostgreSQL 12.5 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit',)

# Following tables were created in the database for the dataset provided by the client:
#############################################################################################
    # 1. Create table: atp_stock (productID | atp_stock | weekId | year)
    create_atp_stock_table = """
            CREATE TABLE IF NOT EXISTS atp_stock (
                productID VARCHAR(20) NOT NULL,
                atp_stock REAL,
                weekId VARCHAR(10) NOT NULL,
                year INT NOT NULL,
                PRIMARY KEY (productID, weekId, year)
            );
    """
    cur.execute(create_atp_stock_table)
    print("Table atp_stock created successfully in PostgreSQL\n")

#############################################################################################
    # 2. Create table: intransit (productID | delivery_amount_sq2 | Eta | weekId | year)
    create_intransit_table = """
            CREATE TABLE IF NOT EXISTS intransit (
                productID VARCHAR(20) NOT NULL,
                delivery_amount_sq2 REAL,
                Eta DATE,
                weekId VARCHAR(10) NOT NULL,
                year INT NOT NULL
            );
    """
    cur.execute(create_intransit_table)
    print("Table intransit created successfully in PostgreSQL\n")

#############################################################################################
    # 3. Create table: ready (productID | readyQty | weekId | year)
    create_ready_table = """
            CREATE TABLE IF NOT EXISTS ready (
                productID VARCHAR(20) NOT NULL,
                readyQty REAL,
                weekId VARCHAR(10) NOT NULL,
                year INT NOT NULL
            );
    """
    cur.execute(create_ready_table)
    print("Table ready created successfully in PostgreSQL\n")

#############################################################################################
    # 4. Create table: sales (productID | Weekly_sales | weekId | year)
    create_sales_table = """
            CREATE TABLE IF NOT EXISTS sales (
                productID VARCHAR(20) NOT NULL,
                Weekly_sales REAL,
                weekId VARCHAR(10) NOT NULL,
                year INT NOT NULL,
                PRIMARY KEY (productID, weekId, year)
            );
    """
    cur.execute(create_sales_table)
    print("Table sales created successfully in PostgreSQL\n")

#############################################################################################
    # 5. Create table: to_be_produced (productID | To_be_produced_sq2 | Etd | weekId | year)
    create_to_be_produced_table = """
            CREATE TABLE IF NOT EXISTS to_be_produced (
                productID VARCHAR(20) NOT NULL,
                To_be_produced_sq2 REAL,
                Etd DATE,
                weekId VARCHAR(10) NOT NULL,
                year INT NOT NULL
            );
    """
    cur.execute(create_to_be_produced_table)
    print("Table to_be_produced created successfully in PostgreSQL\n")

# Following tables were created for in case of need:
#############################################################################################
    # 1. Create table: users (userID | userName | password | name | surname | email)
    create_user_table = """
                CREATE TABLE IF NOT EXISTS users (
                    userID VARCHAR(20) PRIMARY KEY NOT NULL,
                    userName VARCHAR(20) NOT NULL,
                    password VARCHAR(20) NOT NULL,
                    name VARCHAR(20) NOT NULL,
                    surname VARCHAR(20) NOT NULL,
                    email VARCHAR(50) NOT NULL
                );
        """
    cur.execute(create_user_table)
    print("Table users created successfully in PostgreSQL\n")

#############################################################################################
    # 2. Create table: roles (roleID | roleName)
    create_roles_table = """
                    CREATE TABLE IF NOT EXISTS roles (
                        roleID VARCHAR(20) PRIMARY KEY NOT NULL,
                        roleName VARCHAR(20) NOT NULL
                    );
            """
    cur.execute(create_roles_table)
    print("Table roles created successfully in PostgreSQL\n")

#############################################################################################
    # 3. Create table: user_roles (userID | roleID)
    create_user_roles_table = """
                        CREATE TABLE IF NOT EXISTS roles (
                            userID VARCHAR(20) NOT NULL,
                            roleID VARCHAR(20) NOT NULL,
                            PRIMARY KEY (userID, roleID),
                            FOREIGN KEY (userID) REFERENCES users(userID),
                            FOREIGN KEY (roleID) REFERENCES roles(roleID)
                        );
                """
    cur.execute(create_user_roles_table)
    print("Table user_roles created successfully in PostgreSQL\n")

#############################################################################################
    # 4. Create table: transportation (tID | transportation_method)
    create_transportation_table = """
                    CREATE TABLE IF NOT EXISTS users (
                        tID INT PRIMARY KEY NOT NULL,
                        transportation_method VARCHAR(20) NOT NULL
                    );
            """
    cur.execute(create_transportation_table)
    print("Table transportation created successfully in PostgreSQL\n")

#############################################################################################
    # 5. Create table: transportation_archive (tID | annual_capacity_sq2 | cost_per_sq2 | year)
    create_transportation_archive_table = """
                        CREATE TABLE IF NOT EXISTS users (
                            tID INT NOT NULL,
                            annual_capacity_sq2 REAL NOT NULL,
                            cost_per_sq2 REAL NOT NULL,
                            year INT NOT NULL,
                            PRIMARY KEY (tID, year),
                            FOREIGN KEY (tID) REFERENCES transportation(tID)
                        );
                """
    cur.execute(create_transportation_archive_table)
    print("Table transportation_archive created successfully in PostgreSQL\n")


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