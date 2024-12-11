# -*- coding: utf-8 -*-
"""FinalProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q66EiIY-It8VNCTl-zoxWlizQrSqIXMt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

import pandas as pd
import io

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, classification_report)
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('spotify_songs.csv')
print(df.head())

"""Data Cleaning"""

print(df.head())

print(df.info())

# Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# Drop rows/columns with missing values
df = df.dropna()
print(df)

column_names = df.columns.tolist()
print(column_names)

import seaborn as sns
import matplotlib.pyplot as plt

# List of all variables to include in the heatmap
features = [
    'track_popularity', 'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'duration_ms'
]

# Compute the correlation matrix for the selected features
correlation_matrix = df[features].corr()

# Plot the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Spotify Song Features")
plt.show()

# Outlier adjust/data normalisation
for column in df.select_dtypes(include=[np.number]).columns:
    # IQR for outliers
    q75, q25 = np.percentile(df[column], [75, 25])
    IQR = q75 - q25
    upper_limit = q75 + 3.0 * IQR
    lower_limit = q25 - 3.0 * IQR

    # Replace outliers with the mean of the feature
    mean_value = df[column].mean()
    df[column] = np.where(
        (df[column] > upper_limit) | (df[column] < lower_limit), mean_value, df[column]
    )

    # Check for NaNs after replacing outliers
    print(f"NaNs in {column} after outlier handling:", df[column].isnull().sum())

# Confirm no NaNs left
print("NaNs after outlier removal:", df.isnull().sum())

features = ['danceability', 'energy', 'loudness', 'tempo', 'track_popularity']


plt.figure(figsize=(12, 10))


for i, feature in enumerate(features, 1):
    plt.subplot(3, 2, i)
    sns.histplot(df[feature], kde=True, bins=20, color=sns.color_palette("Set2")[i-1])
    plt.title(f'Distribution of {feature}')

plt.tight_layout()
plt.show()

"""Data Pre-Processing"""

X = df[['danceability', 'energy', 'loudness', 'tempo']]
y = df['track_popularity']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save processed data
processed_data = {
    'X_train': X_train_scaled,
    'X_test': X_test_scaled,
    'y_train': y_train,
    'y_test': y_test
}

"""Linear Regression"""

# Linear regression model
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# Predictions
y_pred_lr = lr_model.predict(X_test_scaled)

# Evaluate
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print("Linear Regression MSE:", mse_lr)
print("Linear Regression R²:", r2_lr)

# Feature importance
feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Coefficient": lr_model.coef_
}).sort_values(by="Coefficient", ascending=False)
print(feature_importance)

from sklearn.metrics import mean_absolute_error
mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = mse_lr ** 0.5
print("Linear Regression MAE:", mae_lr)
print("Linear Regression RMSE:", rmse_lr)

"""Random Forest"""

# RANDOM FOREST REGRESSOR
rf_model = RandomForestRegressor(n_estimators=1000, random_state=42)
rf_model.fit(X_train, y_train)

# Predict
y_pred_rf = rf_model.predict(X_test)

# Evaluate
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print(f'Random Forest Model Evaluation:')
print(f'MAE: {mae_rf:.2f}')
print(f'MSE: {mse_rf:.2f}')
print(f'RMSE: {rmse_rf:.2f}')
print(f'R²: {r2_rf:.2f}')

importances = rf_model.feature_importances_
variable = X.columns
varImp_df = pd.DataFrame({'Variable': variable, 'Importance': importances})
varImp_df = varImp_df.sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(10, 6))
sns.barplot(data=varImp_df, x='Importance', y='Variable')
plt.title('Variable Importance in Random Forest')
plt.show()

"""XGBoost"""

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#XGBoost regressor model
xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)

xgb_model.fit(X_train, y_train)
y_pred = xgb_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"XGBoost MSE: {mse}")
print(f"XGBoost R² Score: {r2}")

import matplotlib.pyplot as plt

xgb.plot_importance(xgb_model)
plt.show()