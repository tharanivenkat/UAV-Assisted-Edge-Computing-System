import random
import time
import base64

# System Parameters
NUM_IOT_DEVICES = 5
NUM_UAVS = 3
NUM_EDGE_SERVERS = 2

# Task Parameters
TASK_MIN_SIZE = 1
TASK_MAX_SIZE = 10
TASK_PRIORITY_LEVELS = [1, 2, 3]

# Edge Server
EDGE_PROCESS_SPEED = 5  # Tasks/sec

# UAV Energy Parameters
UAV_INITIAL_BATTERY = 100  # Max battery units
ENERGY_COST_PER_TASK = 10  # Battery used per task

# --- IoT Device ---
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        size = random.randint(TASK_MIN_SIZE, TASK_MAX_SIZE)
        priority = random.choice(TASK_PRIORITY_LEVELS)
        raw_data = f"Device-{self.id}-Size-{size}-Priority-{priority}"
        encrypted_data = base64.b64encode(raw_data.encode()).decode()
        return {
            "id": self.id,
            "size": size,
            "priority": priority,
            "data": encrypted_data,
            "arrival_time": time.time()
        }

# --- UAV ---
class UAV:
    def __init__(self, id):
        self.id = id
        self.battery = UAV_INITIAL_BATTERY

    def can_accept_task(self, task):
        # Only accept if enough battery, or task is high priority
        return self.battery >= ENERGY_COST_PER_TASK or task["priority"] == 3

    def relay_task(self, task, edge_servers):
        if not self.can_accept_task(task):
            print(f"❌ UAV {self.id} rejected task (Low Battery: {self.battery})")
            return

        self.battery -= ENERGY_COST_PER_TASK
        print(f"🔋 UAV {self.id} relaying task (Battery left: {self.battery})")

        best_server = min(edge_servers, key=lambda s: s.queue_size())
        best_server.process_task(task)

# --- Edge Server ---
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        self.queue.append(task)
        print(f"⚙️ Edge Server {self.id} processing encrypted task...")

        # Simulate processing
        time.sleep(task["size"] / EDGE_PROCESS_SPEED)
        self.queue.pop(0)

        decrypted_data = base64.b64decode(task["data"]).decode()
        completion_time = time.time() - task["arrival_time"]

        print(f"✅ Edge Server {self.id} completed task: {decrypted_data} in {completion_time:.2f}s")

# --- Initialize & Run ---
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

for _ in range(10):
    device = random.choice(iot_devices)
    task = device.generate_task()

    # Pick UAV with max battery that can accept the task
    possible_uavs = [uav for uav in uavs if uav.can_accept_task(task)]
    if possible_uavs:
        selected_uav = max(possible_uavs, key=lambda u: u.battery)
        print(f"📡 IoT Device {device.id} sending task to UAV {selected_uav.id}")
        selected_uav.relay_task(task, edge_servers)
    else:
        print("🚫 No UAV available to handle the task.")

    time.sleep(random.uniform(1, 2))
