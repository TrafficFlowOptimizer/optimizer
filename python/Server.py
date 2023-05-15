import json
import os
import random
import socketserver

from python.Optimizer import Optimizer

HOST, PORT = "localhost", 8000


def clear(idx: int):
    if os.path.exists(f'../minizinc/output/{idx}.txt'):
        os.remove(f'../minizinc/output/{idx}.txt')
    if os.path.exists(f'../minizinc/data/{idx}.dzn'):
        os.remove(f'../minizinc/data/{idx}.dzn')
    if os.path.exists(f'../input_data/{idx}.json'):
        os.remove(f'../input_data/{idx}.json')


def clear_all():
    for idx in range(1000):
        clear(idx)


def prepare_data(configuration: dict):
    conf_string = json.dumps(configuration)
    idx = random.randint(0, 999)
    while os.path.exists(f'../input_data/{idx}.json'):
        idx = random.randint(0, 999)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(conf_string)
    return idx


def solve(idx: int, time: int):
    server.optimizer.solve(idx, seconds_limit=time)
    server.optimizer.show_refactored_output(idx)


class SingleTCPHandler(socketserver.BaseRequestHandler):
    """One instance per connection.  Override handle(self) to customize action."""

    def handle(self):
        load = json.loads(self.request.recv(4016).decode('utf-8'))
        time, configuration = load["time"], load["configuration"]
        print("time:", time)
        print("configuration:", configuration)

        idx = prepare_data(configuration)
        solve(idx, time)

        self.request.send(bytes(json.dumps({"status": "success!",
                                            "lights": open(f'../minizinc/output/{idx}.txt', "r").read()}), 'UTF-8'))
        clear(idx)
        self.request.close()


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.optimizer = Optimizer()


# clear()
server = SimpleServer((HOST, PORT), SingleTCPHandler)
server.serve_forever()
