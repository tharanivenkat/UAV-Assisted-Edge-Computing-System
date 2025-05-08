import random
import time

# Simulation Parameters
NUM_IOT_DEVICES = 5  # Number of IoT devices
NUM_UAVS = 3  # Number of UAVs
NUM_EDGE_SERVERS = 2  # Number of Edge Servers

# Task Parameters
TASK_MIN_SIZE = 1  # Minimum task size
TASK_MAX_SIZE = 10  # Maximum task size
TASK_PRIORITY_LEVELS = [1, 2, 3]  # Task priority (1 = Low, 3 = High)

# Edge Server Parameters
EDGE_PROCESS_SPEED = 5  # Tasks per second processed
MAX_QUEUE_SIZE = 5  # Max tasks Edge Server can queue
MAX_UAV_LOAD = 3  # Max tasks a UAV can handle


# IoT Device Class
class IoTDevice:
    def __init__(self, id):
        self.id = id

    def generate_task(self):
        """Generate a task with random size and priority."""
        task_size = random.randint(TASK_MIN_SIZE, TASK_MAX_SIZE)
        priority = random.choice(TASK_PRIORITY_LEVELS)
        task = {"id": self.id, "size": task_size, "priority": priority, "arrival_time": time.time()}
        return task


# UAV Class
class UAV:
    def __init__(self, id):
        self.id = id
        self.current_load = 0  # Tracks the number of tasks assigned

    def relay_task(self, task, edge_servers):
        """Find the best Edge Server and forward the task if load allows."""
        if self.current_load >= MAX_UAV_LOAD:
            print(f"❌ UAV {self.id} is overloaded and cannot accept task {task}")
            return
        
        best_server = min(edge_servers, key=lambda es: es.queue_size())
        if best_server.queue_size() < MAX_QUEUE_SIZE:
            self.current_load += 1  # Increase UAV load
            best_server.process_task(task)
            print(f"✅ UAV {self.id} sent task {task} to Edge Server {best_server.id}")
            self.current_load -= 1  # Reduce load after sending
        else:
            print(f"❌ No available Edge Server for task {task}")


# Edge Server Class
class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.queue = []

    def queue_size(self):
        return len(self.queue)

    def process_task(self, task):
        """Process a task if queue isn't full."""
        if len(self.queue) >= MAX_QUEUE_SIZE:
            print(f"❌ Edge Server {self.id} queue full, rejecting task {task}")
            return
        
        self.queue.append(task)
        print(f"⚙️ Edge Server {self.id} processing task {task}")

        process_time = task["size"] / EDGE_PROCESS_SPEED
        time.sleep(process_time)  # Simulate processing time
        self.queue.pop(0)

        completion_time = time.time() - task["arrival_time"]
        print(f"✅ Edge Server {self.id} completed task {task} in {completion_time:.2f} seconds")


# Initialize IoT Devices, UAVs, and Edge Servers
iot_devices = [IoTDevice(i) for i in range(NUM_IOT_DEVICES)]
uavs = [UAV(i) for i in range(NUM_UAVS)]
edge_servers = [EdgeServer(i) for i in range(NUM_EDGE_SERVERS)]

# Simulate task generation and processing
for _ in range(10):  # Run 10 task cycles
    iot_device = random.choice(iot_devices)
    task = iot_device.generate_task()

    best_uav = min(uavs, key=lambda uav: uav.current_load)  # Choose least loaded UAV
    print(f"📡 IoT Device {iot_device.id} sent task {task} to UAV {best_uav.id}")

    best_uav.relay_task(task, edge_servers)
    time.sleep(random.uniform(1, 3))  # Simulate task arrival delay