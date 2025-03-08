# Table of Contents for Sprint-4

- [SPRINT-4 Related Workload](#sprint-4-related-workload)
  - [4.2.1. Forecast Algorithms Analysis](#421-forecast-algorithms-analysis)
  - [4.2.1.1. Create View and Trigger for Sales Table](#4211-create-view-and-trigger-for-sales-table)
  - [4.3.1. Generate & Analyze Synthetic Dataset](#431-generate--analyze-synthetic-dataset)
  - [4.3.1.1. Create Synthetic Database & Upload Data](#4311-create-synthetic-database--upload-data)


## 4.2.1. Forecast Algorithms Analysis
1. [Forecast Algorithms Sample](algorithms/forecast_analysis_sample.py)
2. [Forecast Algorithms](algorithms/forecast_analysis.py)  
3. [Forecasting Analysis](algorithms/forecast)
4. [Algorithms Explained.md](algorithms/algorithms.md)

# ## 4.2.1.1. Create View and Trigger for Sales Table

1. [Create View and Triggers](database_scripts/db_create_view_sales.py)


## 4.3.1. Generate & Analyze Synhtetic Dataset

### Scripts Created

1. [Dataset Generator](synthetic_dataset_generator.py)
2. [Dataset Analyzer](synthetic_dataset_analysis.py)
3. [Dataset Pipeline](synthetic_dataset.py)
4. [Transportation Related Stuff](synthetic_dataset.py)

### Datasets Created

1. [atp_stock.csv](synthetic_dataset_data/atp_stock.csv)
2. [atp_stock_last_week.csv](synthetic_dataset_data/atp_stock_last_week.csv)
3. [intransit.csv](synthetic_dataset_data/intransit.csv)
4. [intransit_last_week.csv](synthetic_dataset_data/intransit_last_week.csv)
5. [ready.csv](synthetic_dataset_data/ready.csv)
6. [ready_last_week.csv](synthetic_dataset_data/ready_last_week.csv)
7. [sales.csv](synthetic_dataset_data/sales.csv)
8. [sales_last_week.csv](synthetic_dataset_data/sales_last_week.csv)
9. [to_be_produced.csv](synthetic_dataset_data/to_be_produced.csv)
10. [to_be_produced_last_week.csv](synthetic_dataset_data/to_be_produced_last_week.csv)
11. [transportation_info.csv](synthetic_dataset_data/transportation_info.csv)
12. [transportation_info_archive.csv](synthetic_dataset_data/transportation_info_archive.csv)
    


### Analysis

1. [Plots](synthetic_dataset_analysis/plots)
2. [Data Analysis Report](synthetic_dataset_analysis/data_analysis_report.pdf)


## 4.3.1.1. Create Synthetic Database & Upload Data

### Database Created
        host="db-chainsight-synthetic.cd6k86gwohjc.eu-north-1.rds.amazonaws.com",
        port=5432,
        user="metuCeng",
        password="metu-ceng-chainsight",
        dbname="postgres"

### Scripts Created

1. [Test Connection](database_scripts/db_connection_test.py)
2. [Create Tables](database_scripts/db_create_tables.py)
3. [Load Datasets](database_scripts/db_load_data_to_database.py)


    Database version: ('PostgreSQL 16.3 on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-17), 64-bit',)
    ready table created successfully.
    sales table created successfully.
    to_be_produced table created successfully.
    intransit table created successfully.
    atp_stock table created successfully.
    ready_last_week table created successfully.
    sales_last_week table created successfully.
    to_be_produced_last_week table created successfully.
    intransit_last_week table created successfully.
    atp_stock_last_week table created successfully.
    transportation_info table created successfully.
    transportation_info_archive table created successfully.
    ____________________________________________
    12 tables created successfully.

------------------------------------------------------------------------------------------------------------------------

    Data loaded into intransit successfully with 52000 records. 0 rows skipped.
    Data loaded into sales_last_week successfully with 200 records. 0 rows skipped.
    Data loaded into to_be_produced_last_week successfully with 200 records. 0 rows skipped.
    Data loaded into to_be_produced successfully with 52000 records. 0 rows skipped.
    Data loaded into ready_last_week successfully with 200 records. 0 rows skipped.
    Data loaded into atp_stock successfully with 52000 records. 0 rows skipped.
    Data loaded into atp_stock_last_week successfully with 200 records. 0 rows skipped.
    Data loaded into intransit_last_week successfully with 200 records. 0 rows skipped.
    Data loaded into ready successfully with 52000 records. 0 rows skipped.
    Data loaded into sales successfully with 52000 records. 0 rows skipped.    
    Data loaded into transportation_info successfully with 2 records. 0 rows skipped.
    Data loaded into transportation_info_archive successfully with 10 records. 0 rows skipped.
    12 files loaded successfully.
