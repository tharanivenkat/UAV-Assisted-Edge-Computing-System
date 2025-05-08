import threading
import time
import random

class EdgeServer:
    def __init__(self, id):
        self.id = id
        self.energy = 100

    def process_task(self, task_id):
        if self.energy < 10:
            print(f"⚠️ Server {self.id} low on energy. Recharging...")
            self.recharge()
        print(f"⚙️ Server {self.id} started task {task_id}")
        time.sleep(random.uniform(1, 3))
        self.energy -= random.randint(5, 15)
        print(f"✅ Server {self.id} finished task {task_id}. Energy left: {self.energy}")

    def recharge(self):
        time.sleep(2)
        self.energy = 100
        print(f"🔋 Server {self.id} recharged to 100%.")

# Simulate parallel execution
servers = [EdgeServer(i) for i in range(2)]
threads = []

for i in range(5):
    server = servers[i % 2]
    t = threading.Thread(target=server.process_task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
