import random
import time

# Simulation Parameters
NUM_IOT_DEVICES = 5
NUM_UAVS = 3
NUM_EDGE_SERVERS = 2

# Edge Server Processing Speed (Tasks per second)
EDGE_PROCESS_SPEED = 5

# UAV Load Capacity
UAV_MAX_TASKS = 3  # Max tasks a UAV can handle at a time

# Edge Server Load Capacity
EDGE_MAX_QUEUE = 5  # Max tasks an Edge Server can queue

# IoT Device Class
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        """Generate a task with random size."""
        task_size = random.randint(1, 10)
        return {"id": self.id, "size": task_size, "arrival_time": time.time()}

# UAV Class with Load Balancing
class UAV:
    def __init__(self, id):
        self.id = id
        self.current_tasks = 0

    def relay_task(self, task, edge_servers):
        """Only relay tasks if below max load."""
        if self.current_tasks >= UAV_MAX_TASKS:
            print(f"❌ UAV {self.id} overloaded, task rejected.")
            return False
        
        best_server = min(edge_servers, key=lambda es: es.queue_size())
        if best_server.queue_size() < EDGE_MAX_QUEUE:
            self.current_tasks += 1
            best_server.process_task(task, self)
            return True
        else:
            print(f"❌ No Edge Server available, task dropped.")
            return False

    def task_completed(self):
        """Reduce task count when completed."""
        self.current_tasks -= 1

# Edge Server Class with Load Balancing
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task, uav):
        """Process a task only if queue isn't full."""
        self.queue.append(task)
        print(f"⚙️ Edge Server {self.id} processing task {task}")

        process_time = task["size"] / EDGE_PROCESS_SPEED
        time.sleep(process_time)
        self.queue.pop(0)
        uav.task_completed()

        print(f"✅ Edge Server {self.id} completed task {task}")

# Initialize Components
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Simulate Task Processing
for _ in range(10):
    iot_device = random.choice(iot_devices)
    task = iot_device.generate_task()
    best_uav = min(uavs, key=lambda uav: uav.current_tasks)

    print(f"📡 IoT Device {iot_device.id} sending task {task} to UAV {best_uav.id}")
    best_uav.relay_task(task, edge_servers)
    time.sleep(random.uniform(1, 3))