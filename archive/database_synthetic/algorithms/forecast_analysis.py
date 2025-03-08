#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-2 : Conduct a literature review on heuristic approaches for               #
#                       supply chain problems to support development and documentation      #
# issue-1 : compare forecasting algorithms: ARIMA, SARIMA, Holt-Winters                     #
#############################################################################################



import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Define input and output directories
input_folder = '../synthetic_dataset_data/'
output_folder = 'forecast/'

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# List all CSV files excluding '_last_week'
all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv') and not f.endswith('_last_week.csv')]

# Function to evaluate models
def evaluate_model(true, predicted):
    mse = mean_squared_error(true, predicted)
    mae = mean_absolute_error(true, predicted)
    return mse, mae

# Process each file
results = []
best_models = []
for file in all_files:
    # Load data
    file_path = os.path.join(input_folder, file)
    data = pd.read_csv(file_path)

    # Check for year and week columns
    if 'year' not in data.columns or 'weekId' not in data.columns:
        print(f"Skipping {file}: Missing 'year' or 'week' columns.")
        continue

    # Generate date column as 'yyyy-mm-dd' (Monday of the given week)
    data['date'] = pd.to_datetime(data['year'].astype(str) + data['weekId'].astype(str) + '-1', format='%Y%W-%w')
    data.set_index('date', inplace=True)

    # Ensure data is sorted by date
    data = data.sort_index()

    # Select the target column for forecasting
    target_column = 'quantity'  # Explicitly set the target column to 'quantity'

    # Handle non-numeric values by coercing to NaN and forward filling
    data[target_column] = pd.to_numeric(data[target_column], errors='coerce').ffill()

    # Train-test split
    train, test = data[target_column].iloc[:-14], data[target_column].iloc[-14:]

    # Print top 10 values of train and test data
    print(f"File: {file}")
    print("Train Data (Top 10):")
    print(train.head(10))
    print("Test Data (Top 10):")
    print(test.head(10))

    # Ensure data type compatibility
    train = train.astype(float)
    test = test.astype(float)

    # Skip files with insufficient data for seasonal models
    if len(train) < 14:
        print(f"Skipping {file}: Insufficient data for training.")
        continue
    else:
        print(f"Training data size: {len(train)}")

    # ARIMA Model
    print("Fitting ARIMA model...")
    arima_model = ARIMA(train, order=(2, 1, 2))
    arima_fit = arima_model.fit()
    arima_forecast = arima_fit.forecast(steps=14)

    # SARIMA Model
    print("Fitting SARIMA model...")
    sarima_model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7), enforce_stationarity=False, enforce_invertibility=False)
    sarima_fit = sarima_model.fit()
    sarima_forecast = sarima_fit.forecast(steps=14)

    # Holt-Winters Model
    print("Fitting Holt-Winters model...")
    try:
        holt_winters = ExponentialSmoothing(train, seasonal='add', seasonal_periods=7, trend='add')
        hw_fit = holt_winters.fit()
        hw_forecast = hw_fit.forecast(steps=14)
        print("Holt-Winters model fitted successfully.")
    except ValueError:
        print(f"Skipping Holt-Winters model for {file}: Insufficient data for seasonal periods.")
        hw_forecast = np.nan * np.ones(14)

    # Calculate metrics
    arima_mse, arima_mae = evaluate_model(test, arima_forecast)
    sarima_mse, sarima_mae = evaluate_model(test, sarima_forecast)
    hw_mse, hw_mae = evaluate_model(test, hw_forecast)

    # Append results
    results.append([file, 'ARIMA', arima_mse, arima_mae])
    results.append([file, 'SARIMA', sarima_mse, sarima_mae])
    results.append([file, 'Holt-Winters', hw_mse, hw_mae])

    # Determine the best model
    mse_scores = {'ARIMA': arima_mse, 'SARIMA': sarima_mse, 'Holt-Winters': hw_mse}
    best_model = min(mse_scores, key=mse_scores.get)
    best_models.append([file, best_model])

    # Plot Results
    plt.figure(figsize=(14, 8))
    plt.plot(train, label='Train Data', alpha=0.5)
    plt.plot(test, label='Test Data', color='gray', linewidth=2)
    plt.plot(test.index, arima_forecast, label='ARIMA Forecast', linestyle='--', linewidth=2)
    plt.plot(test.index, sarima_forecast, label='SARIMA Forecast', linestyle='-.', linewidth=2)
    if not np.isnan(hw_forecast).all():
        plt.plot(test.index, hw_forecast, label='Holt-Winters Forecast', linestyle='-', linewidth=2, alpha=0.7)
    plt.legend()
    plt.title(f"Forecasting Comparison: {file} (Best: {best_model})")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f"{file}_forecast_plot.png"))
    plt.close()

    print("Analysis completed for", file)

# Store results in a DataFrame
results_df = pd.DataFrame(results, columns=['File', 'Model', 'MSE', 'MAE'])
best_models_df = pd.DataFrame(best_models, columns=['File', 'Best Model'])

# Save results to CSV
results_df.to_csv(os.path.join(output_folder, 'forecasting_results.csv'), index=False)
best_models_df.to_csv(os.path.join(output_folder, 'best_models.csv'), index=False)

print("Analysis completed. Results saved in output folder.")
