#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-3 : Search for external datasets and                                      #
#                       assess their suitability for use in the project.                    #
# issue-1 : generate a synthetic dataset and analyze it                                     #
# function-2 : analyze synthetic data generated                                             #
#############################################################################################

#############################################################################################
import pandas as pd
import os
import matplotlib.pyplot as plt
from synthetic_dataset_generator import get_data_config
from fpdf import FPDF

#############################################################################################
# Function to generate histogram
def generate_histogram(df, dataset_name, analysis_dir):
    plt.figure(figsize=(8, 6))
    plt.hist(df['quantity'], bins=20, edgecolor='k', alpha=0.7)
    plt.title(f'{dataset_name.upper()} - Quantity Distribution')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.grid(True)
    hist_path = os.path.join(analysis_dir, f"{dataset_name}_hist.png")
    plt.savefig(hist_path)
    plt.close()
    return hist_path

#############################################################################################
# Function to generate boxplot
def generate_boxplot(df, dataset_name, analysis_dir):
    plt.figure(figsize=(8, 6))
    plt.boxplot(df['quantity'], vert=False, patch_artist=True)
    plt.title(f'{dataset_name.upper()} - Quantity Boxplot')
    plt.xlabel('Quantity')
    plt.grid(True)
    boxplot_path = os.path.join(analysis_dir, f"{dataset_name}_boxplot.png")
    plt.savefig(boxplot_path)
    plt.close()
    return boxplot_path

#############################################################################################
# Function to generate PDF report for all datasets
def generate_combined_pdf_report(dataset_reports, analysis_dir, report_name="combined_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=1, margin=15)
    pdf.set_font("Times", size=12)

    for report in dataset_reports:
        dataset_name, stats, hist_path, boxplot_path, unique_values, null_values, sample_records = report

        # Page 1 - Sequential Statistics
        pdf.add_page()
        pdf.set_font("Times", 'B', 14)
        pdf.cell(200, 10, f"Statistics Report for {dataset_name.upper()} Dataset", 0, 1, 'C')
        pdf.ln(10)

        # 1. General Overview
        pdf.set_font("Times", 'B', 12)
        pdf.cell(0, 10, '1. General Overview:', 0, 1)
        pdf.set_font("Times", size=10)
        pdf.multi_cell(0, 10, str(stats))
        pdf.ln(5)

        # 2. Sample Records
        pdf.set_font("Times", 'B', 12)
        pdf.cell(0, 10, '2. Sample Records:', 0, 1)
        pdf.set_font("Times", size=10)
        pdf.multi_cell(0, 10, sample_records)
        pdf.ln(5)

        # 3. Unique Values
        pdf.set_font("Times", 'B', 12)
        pdf.cell(0, 10, '3. Unique Values:', 0, 1)
        pdf.set_font("Times", size=10)
        pdf.multi_cell(0, 10, str(unique_values))
        pdf.ln(5)

        # 4. Null Values
        pdf.set_font("Times", 'B', 12)
        pdf.cell(0, 10, '4. Null Values:', 0, 1)
        pdf.set_font("Times", size=10)
        pdf.multi_cell(0, 10, str(null_values))

        # Page 2 - Visualizations (Sequential)
        pdf.add_page()
        pdf.set_font("Times", 'B', 14)
        pdf.cell(200, 10, f'{dataset_name.upper()} - Visualizations', 0, 1, 'C')
        pdf.ln(10)
        pdf.image(hist_path, x=10, y=20, w=180)
        pdf.ln(120)  # Space between plots
        pdf.image(boxplot_path, x=10, y=150, w=180)

    # Save combined PDF
    output_path = os.path.join(analysis_dir, report_name)
    pdf.output(output_path)
    print(f"Analysis report saved as {output_path}")

#############################################################################################
# Function to analyze dataset
def dataset_statistics(dataset_name, data_config, dataset_dir, analysis_dir):
    # Create plots directory under output_dir
    plots_dir = os.path.join(analysis_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    # Load dataset
    config = data_config[dataset_name]
    file_path = os.path.join(dataset_dir, f"{dataset_name}.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    df = pd.read_csv(file_path)

    if 'quantity' in df.columns:
        # Generate statistics
        stats = df['quantity'].describe()

        # Generate visualizations
        hist_path = generate_histogram(df, dataset_name, plots_dir)
        boxplot_path = generate_boxplot(df, dataset_name, plots_dir)

        # Collect additional info
        unique_values = df.nunique()
        null_values = df.isnull().sum()
        sample_records = df.head(5).to_string(index=False)

        return dataset_name, stats, hist_path, boxplot_path, unique_values, null_values, sample_records
    else:
        print("No 'quantity' column found.")
        return None
