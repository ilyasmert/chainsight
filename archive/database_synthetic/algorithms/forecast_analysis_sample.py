#############################################################################################
# created by Kıvanç Filizci on 05 Jan 2025                                                  #
# SPRINT-4 : ITEM-2 : Conduct a literature review on heuristic approaches for               #
#                       supply chain problems to support development and documentation      #
# issue-1 : compare forecasting algorithms: ARIMA, SARIMA, Holt-Winters                     #
#############################################################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Generate synthetic time series data
np.random.seed(42)
data = 50 + np.cumsum(np.random.randn(10000))
dates = pd.date_range(start='2023-01-01', periods=10000, freq='W')
ts = pd.Series(data, index=dates)

# Display 10 samples from the data
print("Sample Data:")
print(ts.head(10))

# Split data into train and test
train, test = ts[:-14], ts[-14:]

# ARIMA Example
arima_model = ARIMA(train, order=(2, 1, 2))
arima_fit = arima_model.fit()
arima_forecast = arima_fit.forecast(steps=14)

# SARIMA Example
sarima_model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
sarima_fit = sarima_model.fit()
sarima_forecast = sarima_fit.forecast(steps=14)

# Holt-Winters Example
holt_winters = ExponentialSmoothing(train, seasonal='add', seasonal_periods=7, trend='add')
hw_fit = holt_winters.fit()
hw_forecast = hw_fit.forecast(steps=14)

# Calculate Errors
arima_mse = mean_squared_error(test, arima_forecast)
arima_mae = mean_absolute_error(test, arima_forecast)

sarima_mse = mean_squared_error(test, sarima_forecast)
sarima_mae = mean_absolute_error(test, sarima_forecast)

hw_mse = mean_squared_error(test, hw_forecast)
hw_mae = mean_absolute_error(test, hw_forecast)

# Print Errors
print("ARIMA - MSE:", arima_mse, "MAE:", arima_mae)
print("SARIMA - MSE:", sarima_mse, "MAE:", sarima_mae)
print("Holt-Winters - MSE:", hw_mse, "MAE:", hw_mae)

# Determine the best algorithm based on MSE
best_model = "ARIMA"
if sarima_mse < arima_mse and sarima_mse < hw_mse:
    best_model = "SARIMA"
elif hw_mse < arima_mse and hw_mse < sarima_mse:
    best_model = "Holt-Winters"

print(f"Best Model: {best_model}")

# Plot Results
plt.figure(figsize=(14, 8))
#plt.plot(train, label='Train Data', alpha=0.5)
plt.plot(test, label='Test Data', color='gray', linewidth=2)
plt.plot(test.index, arima_forecast, label='ARIMA Forecast', linestyle='--', linewidth=2)
plt.plot(test.index, sarima_forecast, label='SARIMA Forecast', linestyle='-.', linewidth=2)
plt.plot(test.index, hw_forecast, label='Holt-Winters Forecast', linestyle='-', linewidth=2, alpha=0.7)
plt.legend()
plt.title(f"Forecasting Comparison: ARIMA, SARIMA, Holt-Winters (Best: {best_model})")
plt.xlabel("Time")
plt.ylabel("Values")
plt.grid(True)
plt.tight_layout()
plt.show()

print("Basic examples for ARIMA, SARIMA, and Holt-Winters completed.")
