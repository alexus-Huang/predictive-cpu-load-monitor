import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = pd.read_csv("data/telemetry.csv")
df['cpu_rolling_avg'] = df['cpu_percent'].rolling(window=5).mean()
df['cpu_trend'] = df['cpu_percent'].diff()

# Create target column
N = 10 # predicting 10 seconds ahead
df['target_cpu'] = df['cpu_percent'].shift(-N)

df = df.dropna() # Nans appear because the last N rows can't shift forward since theres no data N rows ahead. Those rows get Nan in target_cpu and a model isn't able to train on missing labels so I dropped them

X = df[['cpu_percent', 'ram_percent', 'cpu_rolling_avg', 'cpu_trend']]
y = df['target_cpu']
X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=8)

# Fit model
model = LinearRegression()
model.fit(X_train,y_train)

# Evalutae
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
print(f"MAE: {mae:.2f}") # how off the predictions are in %
print(f"MSE: {mse:.2f}")
print(f"cpu_percent std: {df['cpu_percent'].std()}")
# Save model
joblib.dump(model, 'models/thermal_model.pkl')