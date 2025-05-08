from sklearn.linear_model import LinearRegression
import numpy as np

# Simulated historical data (tasks, load)
tasks = np.array([[5], [10], [15], [20], [25]])
load = np.array([10, 20, 30, 40, 50])

model = LinearRegression().fit(tasks, load)

# Predict future load
future_tasks = np.array([[12]])
predicted_load = model.predict(future_tasks)

print(f"📊 Predicted Load for 12 incoming tasks: {predicted_load[0]:.2f}")
