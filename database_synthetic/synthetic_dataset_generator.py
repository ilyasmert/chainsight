#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : generate a synthetic dataset and analyze it                                     #
# function-1 : generate synthetic data for the database tables                              #
#############################################################################################

#############################################################################################
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import os

#############################################################################################
# Generator functions to be used in the data generation process

# 1. product_id_generator: Generates unique product IDs in the format prod-XX-0000
def product_id_generator(num_products):
    # Ensure uniqueness of the product IDs
    product_ids = set()

    while len(product_ids) < num_products:
        category = ''.join(random.choices(string.ascii_uppercase, k=2))  # XX
        number = ''.join(random.choices(string.digits, k=4))             # 0000
        product_id = f'prod-{category}-{number}'
        product_ids.add(product_id)
    return list(product_ids)

# 2. date_generator: Generates a random date in the format dd.mm.yyyy
def date_generator(year, week_number):
    base_date = datetime(year, 1, 1) + timedelta(weeks=week_number - 1)
    return (base_date + timedelta(weeks=np.random.randint(0, 9))).strftime('%d.%m.%Y')

# 3. quantity_generator: Generates a random quantity within a specified range
def quantity_generator(min_val=0, max_val=10001):
    return lambda: np.random.randint(min_val, max_val)

#############################################################################################
# Generic data generator
def generic_data_generator(dataset_name, config, product_ids, total_weeks, start_year, weeks_per_year, output_dir):
    # Generate data for datasets with configurable structures
    data = []
    for week in range(total_weeks):
        year = start_year + (week // weeks_per_year)
        week_number = (week % weeks_per_year) + 1  # Week number in the year
        for product in product_ids:
            quantity = config.get('quantity_generator', quantity_generator(0, 200))()
            row = [product, quantity, week_number, year]

            # Add extra columns if specified in the configuration
            if 'date_generator' in config:
                date_value = config['date_generator'](year, week_number)
                row.append(date_value)

            data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data, columns=config['columns'])

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{dataset_name}.csv")

    # Export to CSV
    df.to_csv(output_file, index=False)
    print(f"{dataset_name.upper()} dataset saved as {output_file}")

#############################################################################################
# Example dataset configurations
def get_data_config():
    return {
        'ready': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_ready_data.csv',
            'quantity_generator': quantity_generator(0, 10001)  # Non-negative
        },
        'sales': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_sales_data.csv',
            'quantity_generator': quantity_generator(0, 5001)  # Sales-specific
        },
        'to_be_produced': {
            'columns': ['productId', 'quantity', 'weekId', 'year', 'ETD'],
            'output_file': 'synthetic_to_be_produced_data.csv',
            'date_generator': date_generator
        },
        'intransit': {
            'columns': ['productId', 'quantity', 'weekId', 'year', 'ETA'],
            'output_file': 'synthetic_intransit_data.csv',
            'date_generator': date_generator
        },
        'atp_stock': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_atp_stock_data.csv',
            'quantity_generator': quantity_generator(-5000, 10001)  # Can be negative
        },
        'ready_last_week': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_ready_data.csv',
            'quantity_generator': quantity_generator(0, 10001)  # Non-negative
        },
        'sales_last_week': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_sales_data.csv',
            'quantity_generator': quantity_generator(0, 5001)  # Sales-specific
        },
        'to_be_produced_last_week': {
            'columns': ['productId', 'quantity', 'weekId', 'year', 'ETD'],
            'output_file': 'synthetic_to_be_produced_data.csv',
            'date_generator': date_generator
        },
        'intransit_last_week': {
            'columns': ['productId', 'quantity', 'weekId', 'year', 'ETA'],
            'output_file': 'synthetic_intransit_data.csv',
            'date_generator': date_generator
        },
        'atp_stock_last_week': {
            'columns': ['productId', 'quantity', 'weekId', 'year'],
            'output_file': 'synthetic_atp_stock_data.csv',
            'quantity_generator': quantity_generator(-5000, 10001)  # Can be negative
        }
    }

#############################################################################################
