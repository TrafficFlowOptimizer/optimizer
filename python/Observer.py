import time
import os
from threading import Thread

from python.Optimizer import Optimizer


class Observer:
    def __init__(self):
        self.tasks = []
        self.server_running = False

    def add_task(self, id: int):
        self.tasks.append(id)

    def start_server(self):
        self.add_task(936)
        # self.add_task(936)
        self.server_running = True
        # os.system("uvicorn Server:app --reload")

    def wait_for_tasks(self):
        while True:
            if len(self.tasks) > 0:
                task = self.tasks.pop(0)
                print(f'starting optimization for {task}')
                optimizer = Optimizer()
                optimizer.provide_data(f'../minizinc/data/{task}.dzn', task, 2)
                optimizer.solve(f'../minizinc/output/{task}.txt', 10)

            else:
                print("empty!")
            time.sleep(1.5)
            print("--")
            time.sleep(0.5)

    def run(self):
        os.system("echo Hello from the other side!")
        t = Thread(self.start_server)
        t2 = Thread(target=self.wait_for_tasks)
        t.start()
        t2.start()
        t.join()
        t2.join()


# observer = Observer()
# observer.run()

optimizer = Optimizer()
optimizer.provide_data(f'../minizinc/data/{936}.dzn', 936, 2)
optimizer.solve(f'../minizinc/output/{936}.txt', 10)