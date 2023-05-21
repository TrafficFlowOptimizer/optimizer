import json
import os
import socketserver
from glob import glob
from uuid import uuid4

from python.Optimizer import Optimizer
from python.Utils import prepare_output_for_backend

HOST, PORT = "localhost", 8000


def clear(idx: int):
    if os.path.exists(f'../minizinc/output/{idx}.txt'):
        os.remove(f'../minizinc/output/{idx}.txt')
    if os.path.exists(f'../minizinc/data/{idx}.dzn'):
        os.remove(f'../minizinc/data/{idx}.dzn')
    if os.path.exists(f'../input_data/{idx}.json'):
        os.remove(f'../input_data/{idx}.json')


def clear_all():
    fileList = glob('../minizinc/output/[0-9]*.txt')
    fileList += glob('../minizinc/data/[0-9]*.dzn')
    fileList += glob('../input_data/[0-9]*.json')
    print(fileList)
    for filePath in fileList:
        if os.path.exists(filePath):
            os.remove(filePath)


def prepare_data(configuration: dict):
    conf_string = json.dumps(configuration)
    idx = uuid4().int >> (128 - 24)
    while os.path.exists(f'../input_data/{idx}.json'):
        idx = uuid4().int >> (128 - 24)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(conf_string)
    return idx


def solve(idx: int, time: int):
    server.optimizer.solve(idx, seconds_limit=time)
    # server.optimizer.show_raw_output(idx)
    # server.optimizer.show_refactored_output(idx)


class SingleTCPHandler(socketserver.BaseRequestHandler):
    """One instance per connection.  Override handle(self) to customize action."""

    def handle(self):
        load = json.loads(self.request.recv(4016).decode('utf-8'))
        time, configuration = load["time"], load["configuration"]
        print("time:", time)
        print("configuration:", configuration)

        idx = prepare_data(configuration)
        solve(idx, time)

        data = prepare_output_for_backend(f'../minizinc/output/{idx}.txt')
        for dict in data["results"]:
            for key, value in dict.items():
                print(key, ':', value)
            print()

        self.request.send(bytes(json.dumps(data), 'UTF-8'))
        clear(idx)
        self.request.close()


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.optimizer = Optimizer()


# clear_all()
server = SimpleServer((HOST, PORT), SingleTCPHandler)
server.serve_forever()
