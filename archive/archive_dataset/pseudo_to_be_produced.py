# created by Kıvanç Filizci on 22 Nov 2024
# SPRINT-2 : ITEM-4 : creating pseudo datasets_old for the project
# generate pseudo to-be-produced data for the project since the real data is not provided yet

import pandas as pd
import os
import random
from datetime import datetime, timedelta

# Define the directory and file name
output_directory = 'datasets_pseudo'
output_file = 'to-be-produced.xlsx'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Function to calculate week number based on date
def calculate_week_number(date):
    start_of_year = datetime(date.year, 1, 1)
    return ((date - start_of_year).days // 7) + 1

# Generate sample data
data = {
    'productId': [f'P{i:04d}' for i in range(1, 501)],
    'product': [f'Product {i}' for i in range(1, 501)],
    'quantity (sq2)': [random.uniform(1, 1000) for _ in range(500)],
    'etp': [(datetime.now() - timedelta(days=random.randint(1, 365))) for _ in range(500)],
    'year': [2024] * 500
}

# Calculate weekNumber based on etp
data['weekNumber'] = [calculate_week_number(etp) for etp in data['etp']]

# Convert etp to string format
data['etp'] = [etp.strftime('%Y-%m-%d') for etp in data['etp']]

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel(os.path.join(output_directory, output_file), index=False)