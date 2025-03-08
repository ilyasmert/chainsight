#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : generate a synthetic dataset and analyze it                                     #
# function-4 : script to generate synthetic dataset for transportation related tables       #
#############################################################################################

#############################################################################################
import pandas as pd
from datetime import datetime

#############################################################################################
# Define current year
current_year = datetime.today().year

#############################################################################################
# Define transportation properties
transportation_properties = {
    'Truck': {
        'transportationId': 'TR-01',
        'transportationName': 'Truck',
        'transportationCapacity': [7500, 9000, 10500, 12000, 14000, 15000],  # capacities in sq2 for 2020-2025
        'transportationCost': [2500, 3000, 3500, 4000, 4500, 5000]             # costs for 2020-2025
    },
    'Container': {
        'transportationId': 'TR-02',
        'transportationName': 'Container',
        'transportationCapacity': [70000, 80000, 90000, 120000, 135000, 150000],  # capacities in sq2 for 2020-2025
        'transportationCost': [900, 1000, 1100, 1250, 1400, 1500]                    # costs for 2020-2025
    }
}

# Generate data for transportation_info (current year only)
transportation_info = []
for key, props in transportation_properties.items():
    index = current_year - 2020
    transportation_info.append({
        'transportationId': props['transportationId'],
        'transportationName': props['transportationName'],
        'transportationCapacity': props['transportationCapacity'][index],
        'transportationCost': props['transportationCost'][index],
        'year': current_year
    })

# Create a DataFrame for transportation_info
df_transportation_info = pd.DataFrame(transportation_info)

# Generate data for transportation_info_archive (past years: 2022-2024)
years = list(range(2020, 2025))
transportation_info_archive = []
for year in years:
    for key, props in transportation_properties.items():
        index = year - 2020
        transportation_info_archive.append({
            'transportationId': props['transportationId'],
            'transportationName': props['transportationName'],
            'transportationCapacity': props['transportationCapacity'][index],
            'transportationCost': props['transportationCost'][index],
            'year': year,
            'archiveDate': datetime.today().strftime('%Y-%m-%d')
        })

# Create a DataFrame for transportation_info_archive
df_transportation_info_archive = pd.DataFrame(transportation_info_archive)

# Save data to CSV files
info_file = 'synthetic_dataset_data/transportation_info.csv'
archive_file = 'synthetic_dataset_data/transportation_info_archive.csv'

df_transportation_info.to_csv(info_file, index=False)
df_transportation_info_archive.to_csv(archive_file, index=False)

print(f"Files saved: {info_file}, {archive_file}")
