# Loading the necessary libraries
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Loading the dataset
data = pd.read_excel('data/UAE_Population_data.xlsx')

# Check basic structure of the data
print(data.head())
print(data.info())

# Preprocessing the Data 
# preprocessing the data for time series forecasting or regression modeling.
##############################################

# Convert 'year' to datetime 
data['year'] = pd.to_datetime(data['year'], format='%Y')

# Drop missing values 
data.dropna(inplace=True)

# For time series, we'll group the data by year and sum population
population_year = data.groupby('year')['value'].sum().reset_index()

# Check the result
print(population_year.head())

#Time Series Forecasting (ARIMA)
# to predict future population growth based on historical data
##############################################

# Set the 'year' column as the index
population_year.set_index('year', inplace=True)

# ARIMA Model for Time Series Forecasting
model = ARIMA(population_year['value'], order=(5, 1, 0))  # Adjust (p, d, q) parameters based on model performance
model_fit = model.fit()

# Make predictions
forecast = model_fit.forecast(steps=10)  # Forecast the next 10 years

# Plotting the forecast
plt.plot(population_year.index, population_year['value'], label='Historical Data')
plt.plot(pd.date_range(start=population_year.index[-1], periods=11, freq='Y')[1:], forecast, label='Forecast', color='red')
plt.title('UAE Population Forecast')
plt.xlabel('Year')
plt.ylabel('Population')
plt.legend()
plt.show()

# Print the forecasted values
print(forecast)

# Regression Modeling
# to predict population based on year, gender, and age group.
###############################

# Prepare data for regression modeling
# Ensure that the 'year' column is treated numerically
data['year'] = data['year'].dt.year

# Convert categorical columns to dummy/one-hot encoding
X = pd.get_dummies(data[['year', 'sex', 'age_group_name']], drop_first=True)

# Check the data types of the feature matrix
print(X.dtypes)

# Verify the target variable is numeric
y = data['value']
print(y.dtypes)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
lr_rmse = mean_squared_error(y_test, y_pred_lr, squared=False)
lr_r2 = r2_score(y_test, y_pred_lr)

print(f'Linear Regression RMSE: {lr_rmse}')
print(f'Linear Regression R-squared: {lr_r2}')

# Random Forest Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred_rf = rf_model.predict(X_test)

# Evaluate the model
rf_rmse = mean_squared_error(y_test, y_pred_rf, squared=False)
rf_r2 = r2_score(y_test, y_pred_rf)

print(f'Random Forest RMSE: {rf_rmse}')
print(f'Random Forest R-squared: {rf_r2}')

# Model Evaluation and Insights
# comparing the results of the models

# Compare RMSE and R-squared values for both models
print(f'Linear Regression RMSE: {lr_rmse}, R2: {lr_r2}')
print(f'Random Forest RMSE: {rf_rmse}, R2: {rf_r2}')

# Analyze the importance of different features to understand which factors contribute the most to the population predictions.
feature_importances = rf_model.feature_importances_
feature_names = X.columns

# Create a DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

print(importance_df)

# Plotting the predicted values vs the actual values to visually inspect the model’s performance.
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Population')
plt.ylabel('Predicted Population')
plt.title('Actual vs Predicted Population')
plt.grid(True)
plt.show()


