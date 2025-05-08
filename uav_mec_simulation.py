import random
import time

# Defining System Parameters
# Simulation Parameters
NUM_IOT_DEVICES = 5    # Number of IoT devices
NUM_UAVS = 2           # Number of UAVs available
NUM_EDGE_SERVERS = 2   # Number of Edge Servers

# Task Parameters
TASK_MIN_SIZE = 1               # Minimum task size (CPU cycles)
TASK_MAX_SIZE = 10              # Maximum task size (CPU cycles)
TASK_GENERATION_TIME = (1, 3)    # Time range for IoT devices to generate tasks

# UAV Parameters
UAV_TRANSMISSION_TIME = (1, 3)  # Time UAV takes to relay a task

# Edge Server Parameters
EDGE_PROCESS_TIME = (2, 5)    # Time to process a task at an Edge Server

# Defining IoT Device Behavior
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        task_size = random.randint(TASK_MIN_SIZE, TASK_MAX_SIZE)
        print(f"[{time.time():.2f}s] IoT Device {self.id} generated task of size {task_size}")
        return {"id": self.id, "size": task_size, "arrival_time": time.time()}  # Corrected dictionary return format


# Defining UAV Behavior
class UAV:
    def __init__(self, id):
        self.id = id

    def relay_task(self, task, edge_servers):
        print(f"[{time.time():.2f}s] UAV {self.id} picked up task from IoT Device {task['id']}")
        time.sleep(random.uniform(*UAV_TRANSMISSION_TIME))  # Simulate UAV travel time

        # Find the Edge Server with the fewest tasks in queue
        best_server = min(edge_servers, key=lambda es: es.queue_size())
        best_server.process_task(task)


# Defining Edge Server Behavior
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []  # Task queue

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        self.queue.append(task)
        print(f"[{time.time():.2f}s] Edge Server {self.id} started processing task from IoT Device {task['id']}")

        process_time = random.uniform(*EDGE_PROCESS_TIME)
        time.sleep(process_time)  # Simulate processing delay
        self.queue.pop(0)

        completion_time = time.time() - task["arrival_time"]
        print(f"[{time.time():.2f}s] Edge Server {self.id} completed task in {completion_time:.2f} seconds")


# Simulating the Task Offloading Process
# Create IoT Devices, UAVs, and Edge Servers
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Simulate task generation and processing
for _ in range(10):  # Simulate 10 task cycles
    iot_device = random.choice(iot_devices)
    task = iot_device.generate_task()

    selected_uav = random.choice(uavs)
    selected_uav.relay_task(task, edge_servers)

    time.sleep(random.uniform(*TASK_GENERATION_TIME))  # Wait for the next task
