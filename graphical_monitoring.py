import random
import matplotlib.pyplot as plt

# Simulated performance data
time_stamps = list(range(1, 11))
completion_times = [random.uniform(1, 5) for _ in time_stamps]
energy_levels = [random.randint(30, 100) for _ in time_stamps]

# Plot task completion time
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(time_stamps, completion_times, marker='o', color='blue')
plt.title("Task Completion Time")
plt.xlabel("Time")
plt.ylabel("Completion Time (s)")

# Plot energy levels
plt.subplot(1, 2, 2)
plt.plot(time_stamps, energy_levels, marker='x', color='green')
plt.title("UAV Energy Levels")
plt.xlabel("Time")
plt.ylabel("Energy (%)")

plt.tight_layout()
plt.show()
