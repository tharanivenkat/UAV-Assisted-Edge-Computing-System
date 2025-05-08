import random
import time
import base64

# Simulation Parameters
NUM_IOT_DEVICES = 3
NUM_UAVS = 2
NUM_EDGE_SERVERS = 2

TASK_MIN_SIZE = 1
TASK_MAX_SIZE = 10
EDGE_PROCESS_SPEED = 5

# IoT Device Class
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        task_size = random.randint(TASK_MIN_SIZE, TASK_MAX_SIZE)
        content = f"Task from IoT {self.id} of size {task_size}"
        encoded_content = base64.b64encode(content.encode()).decode()
        task = {
            "id": self.id,
            "size": task_size,
            "data": encoded_content,
            "arrival_time": time.time()
        }
        print(f"🔐 IoT Device {self.id} generated and encrypted task: {content}")
        return task


# UAV Class
class UAV:
    def __init__(self, id):
        self.id = id

    def relay_task(self, task, edge_servers):
        best_server = min(edge_servers, key=lambda es: es.queue_size())
        print(f"📡 UAV {self.id} forwarding encrypted task to Edge Server {best_server.id}")
        best_server.process_task(task)


# Edge Server Class
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        self.queue.append(task)
        decoded_data = base64.b64decode(task["data"]).decode()
        print(f"🛡️ Edge Server {self.id} decrypted task: {decoded_data}")

        process_time = task["size"] / EDGE_PROCESS_SPEED
        time.sleep(process_time)
        self.queue.pop(0)

        completion_time = time.time() - task["arrival_time"]
        print(f"✅ Edge Server {self.id} completed task in {completion_time:.2f} seconds\n")


# Initialize Devices
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Simulation
for _ in range(5):
    device = random.choice(iot_devices)
    task = device.generate_task()
    selected_uav = random.choice(uavs)
    selected_uav.relay_task(task, edge_servers)
    time.sleep(random.uniform(1, 2))