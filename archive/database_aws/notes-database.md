Author: Kıvanç Filizci

This file is created to keep the notes about the SPRINT-3 : ITEM-1 related issues.

____________________________________________________________________________________
## Creating the Template Database

____________________________________________________________________________________
### 3.1.1. x
* The dataset provided by the client was in Excel format.
* The dataset was transformed into CSV format.
* The dataset was split into 5 different CSV files.
* The dataset was transformed into a format that can be used in a relational database.
* **Python scripts used**
  * convert_raw_dataset.py
  ```
    /Users/kivancfk/Desktop/ceng49x/dataset/convert_raw_dataset.py 
    Number of Excel files converted: 5
    Number of Excel files created: 5
    Number of CSV files created: 5
  ```
  * primary_key_check.py
    * primary_key_check_output.txt
  
  

____________________________________________________________________________________
### 3.1.2. Creating the Database
* Relational database will be used in this project.
* The database will be created using PostgreSQL.
* **psycopg2** will be used to connect to the database.

* https://www.youtube.com/watch?v=_Yzr7yBGWQI
* Database was created on AWS RDS, PostgreSQL.
* **database name:** db-chainsight
* **master username:** metuCeng
* **master password:** metu-ceng-chainsight
* **endpoint:** db-chainsight.cd6k86gwohjc.eu-north-1.rds.amazonaws.com

* **Python scripts used**
  * none

____________________________________________________
### 3.1.3.1. Connecting to the Database using pgAdmin
* https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.pgAdmin.html
* https://www.youtube.com/watch?v=_Yzr7yBGWQI
* Connection error: Connection attempt timed out.
* **how to fix:** 
  * Go to the security group of the RDS instance.
  * Add a new inbound rule for the security group.
  * Type: PostgreSQL, Protocol: TCP, Port Range: 5432, Source: Anywhere-IPv4
  * Save the rule.
  * **remarks**: This is not a secure way to connect to the database. It is only for testing purposes.
  * connection was successful.
  


### 3.1.3.2. Connecting to the Database using Python
* https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Connecting.PythonDriver.html
* https://www.youtube.com/watch?v=H7-Nq0sBtV8

    ```python
    pip install psycopg2-binary
    Collecting psycopg2-binary
      Downloading psycopg2_binary-2.9.10-cp312-cp312-macosx_12_0_x86_64.whl.metadata (4.9 kB)
    Downloading psycopg2_binary-2.9.10-cp312-cp312-macosx_12_0_x86_64.whl (3.0 MB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 3.8 MB/s eta 0:00:00
    Installing collected packages: psycopg2-binary
    Successfully installed psycopg2-binary-2.9.10
    
    ```
* connect_to_database.py file was created and implemented.
* connection was successful.
    * Database version: ('PostgreSQL 16.3 on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-17), 64-bit',)

* **Python scripts used**
  * connection_test.py

____________________________________________________________________________________
### 3.1.4. Creating the Tables in the Database
* Following tables were created in the database for the dataset provided by the client:
    * atp_stock
    * intransit
    * ready
    * sales
    * to_be_produced

* Following tables were created for in case of need:
    * users
    * roles
    * user_roles
    * transportation
    * transportation_archive

* **Python scripts used**
  * create_tables.p
  * drop_tables.py
    

____________________________________________________________________________________
### 3.1.5. Inserting Data into the Tables

    /Users/kivancfk/Desktop/algo/pythonProject/.venv/bin/python /Users/kivancfk/Desktop/ceng49x/database/load_data_to_tables.py 
    
    Loading data from 'intransit.csv' into table 'intransit'
        Data from 'intransit.csv' loaded successfully into table 'intransit', 18843 rows inserted
    Loading data from 'to_be_produced.csv' into table 'to_be_produced'
        Data from 'to_be_produced.csv' loaded successfully into table 'to_be_produced', 6600 rows inserted
    Loading data from 'atp_stock.csv' into table 'atp_stock'
        Data from 'atp_stock.csv' loaded successfully into table 'atp_stock', 16881 rows inserted
    Loading data from 'ready.csv' into table 'ready'
        Data from 'ready.csv' loaded successfully into table 'ready', 3767 rows inserted
    Loading data from 'sales.csv' into table 'sales'
        Data from 'sales.csv' loaded successfully into table 'sales', 16880 rows inserted
    Skipped rows saved to 'skipped_rows.csv'


* **Python scripts used**
    * load_data_to_tables.py
    * truncate_tables.py