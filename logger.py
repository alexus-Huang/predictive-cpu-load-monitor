import psutil
import time
import pandas as pd

end_time = time.time() + (15 * 60)
data = []

while time.time() < end_time:
    # Get RAM stats and overall average CPU percent which is simpler for feeding into a model
    data.append({
        'cpu_percent': psutil.cpu_percent(interval=1), 
        'ram_percent':psutil.virtual_memory().percent,
        'time_stamp': time.time()
        })
pd.DataFrame(data).to_csv("data/telemetry.csv", index = False)