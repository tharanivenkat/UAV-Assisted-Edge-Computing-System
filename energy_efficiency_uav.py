import random
import time

# Simulation Parameters
NUM_IOT_DEVICES = 5
NUM_UAVS = 3
NUM_EDGE_SERVERS = 2

# Task Parameters
TASK_MIN_SIZE = 1
TASK_MAX_SIZE = 10
TASK_PRIORITY_LEVELS = [1, 2, 3]

# UAV Parameters
UAV_RANGE = 50
BATTERY_FULL = 100  # Full battery level
BATTERY_CONSUMPTION_PER_TASK = 10  # Battery used per task
BATTERY_THRESHOLD = 20  # Minimum battery to accept tasks

# Edge Server Parameters
EDGE_PROCESS_SPEED = 5

class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        task_size = random.randint(TASK_MIN_SIZE, TASK_MAX_SIZE)
        priority = random.choice(TASK_PRIORITY_LEVELS)
        return {"id": self.id, "size": task_size, "priority": priority, "arrival_time": time.time()}

class UAV:
    def __init__(self, id):
        self.id = id
        self.battery_level = BATTERY_FULL

    def relay_task(self, task, edge_servers):
        if self.battery_level < BATTERY_THRESHOLD:
            print(f"🔋 UAV {self.id} has low battery ({self.battery_level}%), skipping task.")
            return

        best_server = min(edge_servers, key=lambda es: es.queue_size())
        best_server.process_task(task)
        self.battery_level -= BATTERY_CONSUMPTION_PER_TASK
        print(f"✅ UAV {self.id} relayed task to Edge Server {best_server.id}, battery now {self.battery_level}%")

class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        self.queue.append(task)
        print(f"⚙️ Edge Server {self.id} processing task {task}")
        time.sleep(task["size"] / EDGE_PROCESS_SPEED)
        self.queue.pop(0)
        completion_time = time.time() - task["arrival_time"]
        print(f"✅ Edge Server {self.id} completed task in {completion_time:.2f} seconds")

# Initialize devices
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Simulate
for _ in range(10):
    iot_device = random.choice(iot_devices)
    task = iot_device.generate_task()

    available_uavs = [uav for uav in uavs if uav.battery_level >= BATTERY_THRESHOLD]
    if not available_uavs:
        print("⚠️ No UAVs with sufficient battery available.")
        break

    selected_uav = random.choice(available_uavs)
    print(f"📡 IoT Device {iot_device.id} sending task to UAV {selected_uav.id}")
    selected_uav.relay_task(task, edge_servers)
    time.sleep(random.uniform(1, 2))