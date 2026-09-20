from flask import Flask, jsonify, send_from_directory
import psutil
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('models/thermal_model.pkl')

cpu_history = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/telemetry')
def get_telemetry():
    global cpu_history
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    # buffer logic
    cpu_history.append(cpu)
    cpu_history = cpu_history[-5:] # Only need last 5 readings to match rolling(window=5) in training
    cpu_rolling_avg = sum(cpu_history) / len(cpu_history) 
    if len(cpu_history) >=2:
        cpu_trend = cpu_history[-1] - cpu_history[-2]
    else:
        cpu_trend = 0

    features = pd.DataFrame([[cpu, ram, cpu_rolling_avg, cpu_trend]],
                         columns=['cpu_percent', 'ram_percent', 'cpu_rolling_avg', 'cpu_trend'])
    predicted_cpu = model.predict(features)[0] # Gets single value out of the array .predict() returns
    # build feature array and call model.predict()
    return jsonify({
        'current_cpu':cpu,
        'predicted_cpu': round(predicted_cpu, 2),
        'status': 'WARNING' if predicted_cpu > 85 else 'NORMAL'
    })
if __name__ == '__main__':
    app.run(debug=True)