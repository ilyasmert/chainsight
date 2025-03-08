#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : generate a synthetic dataset and analyze it                                     #
# function-3 : main script to generate and analyze synthetic data                           #
#############################################################################################

#############################################################################################
import os
from synthetic_dataset_generator import generic_data_generator, get_data_config, product_id_generator
from synthetic_dataset_analysis import dataset_statistics, generate_combined_pdf_report

#############################################################################################
# Global Parameters
NUM_PRODUCTS = 200                                  # Number of unique products
YEARS = 5                                           # Number of years to generate data for
WEEKS_PER_YEAR = 52                                 # Number of weeks in a year
TOTAL_WEEKS = WEEKS_PER_YEAR * YEARS                # Total number of weeks
START_YEAR = 2020                                   # Starting year for the dataset
PRODUCT_IDS = product_id_generator(NUM_PRODUCTS)    # Generate unique product IDs
DATASET_DIR = 'synthetic_dataset_data/'  # Base directory for datasets
ANALYSIS_DIR = 'synthetic_dataset_analysis/'  # Directory to save plots
REPORT_NAME = "data_analysis_report.pdf"            # Name of the combined report

#############################################################################################
# Ensure directories exist
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

#############################################################################################
# Load dataset configurations
DATA_CONFIG = get_data_config()

#############################################################################################
# Step 1: Generate synthetic datasets
print("Generating synthetic datasets...")
created_datasets = 0
for dataset in DATA_CONFIG.keys():
    # Determine weeks and start year based on dataset type
    if dataset.endswith('_last_week'):
        TOTAL_WEEKS = 1
        START_YEAR = 2025
    else:
        TOTAL_WEEKS = TOTAL_WEEKS
        START_YEAR = START_YEAR

    generic_data_generator(dataset, DATA_CONFIG[dataset], PRODUCT_IDS, TOTAL_WEEKS, START_YEAR, WEEKS_PER_YEAR, DATASET_DIR)
    created_datasets += 1

print(f"Synthetic datasets generation completed. Total datasets created: {created_datasets}")
print("_________________________________________________________________________________________\n")

#############################################################################################
# Step 2: Analyze generated datasets
print("Analyzing synthetic datasets...")
dataset_reports = []

for dataset in DATA_CONFIG.keys():
    report = dataset_statistics(dataset, DATA_CONFIG, DATASET_DIR, ANALYSIS_DIR)
    if report:
        dataset_reports.append(report)

# Generate PDF report
if dataset_reports:
    generate_combined_pdf_report(dataset_reports, ANALYSIS_DIR, report_name=REPORT_NAME)
    print("Analysis completed. Report generated successfully.")
else:
    print("No datasets analyzed. Check dataset generation and configurations.")

print("_________________________________________________________________________________________\n")
#############################################################################################
# End of script