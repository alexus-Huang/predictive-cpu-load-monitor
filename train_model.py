import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = pd.read_csv("data/telemetry.csv")
print(df.head())

# Create target column
N = 10 # predicting 10 seconds ahead
df['target_cpu'] = df['cpu_percent'].shift(-N)

df = df.dropna()

X = df[['cpu_percent','ram_percent']]
y = df['target_cpu']
X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=8)

model = LinearRegression()
model.fit(X_train,y_train)

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)

print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")

joblib.dump(model, 'models/thermal_model.pkl')