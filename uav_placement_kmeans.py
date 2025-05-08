import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Simulated IoT device positions (x, y)
num_devices = 20
iot_positions = np.random.rand(num_devices, 2) * 100  # Coordinates within 100x100 grid

# Number of UAVs to place
num_uavs = 3

# Apply K-Means clustering
kmeans = KMeans(n_clusters=num_uavs, random_state=0).fit(iot_positions)
uav_positions = kmeans.cluster_centers_

# Plotting
plt.scatter(iot_positions[:, 0], iot_positions[:, 1], c='blue', label='IoT Devices')
plt.scatter(uav_positions[:, 0], uav_positions[:, 1], c='red', marker='X', s=200, label='UAVs')
plt.title('UAV Placement Optimization using K-Means')
plt.legend()
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.grid(True)
plt.show()
