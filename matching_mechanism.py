import random
import time

# Simulation Parameters
NUM_IOT_DEVICES = 5  # Number of IoT devices
NUM_UAVS = 3  # Number of UAVs
NUM_EDGE_SERVERS = 2  # Number of Edge Servers

# UAV Parameters
UAV_BATTERY_LEVELS = {i: random.randint(50, 100) for i in range(NUM_UAVS)}  # Battery percentage

# IoT Device Class
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        """Generate a task with random size."""
        task_size = random.randint(1, 10)
        return {"id": self.id, "size": task_size, "arrival_time": time.time()}

# UAV Class
class UAV:
    def __init__(self, id):
        self.id = id

    def relay_task(self, task, edge_servers):
        """Choose the best Edge Server based on queue size."""
        best_server = min(edge_servers, key=lambda es: es.queue_size())
        best_server.process_task(task)
        print(f"UAV {self.id} relayed task {task} to Edge Server {best_server.id}")

# Edge Server Class
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        """Process a task."""
        self.queue.append(task)
        process_time = task["size"] / 5
        time.sleep(process_time)
        self.queue.pop(0)
        print(f"Edge Server {self.id} completed task {task}")

# Initialize Components
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Task Matching and Processing
for _ in range(10):
    iot_device = random.choice(iot_devices)
    task = iot_device.generate_task()
    best_uav = min(uavs, key=lambda uav: UAV_BATTERY_LEVELS[uav.id])  # Select UAV with highest battery
    print(f"IoT Device {iot_device.id} assigned task to UAV {best_uav.id} (Battery: {UAV_BATTERY_LEVELS[best_uav.id]}%)")
    best_uav.relay_task(task, edge_servers)
    time.sleep(random.uniform(1, 3))