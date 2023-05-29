import json
import socket

HOST, PORT = "localhost", 9091


def send_request(path: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        json_data = json.load(open(path))
        data = {
            "time": 10,
            "configuration": json_data
        }
        s.send(bytes(json.dumps(data), 'UTF-8'))

        received = json.loads(s.recv(4016).decode('UTF-8'))

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))


send_request("../input_data/data_kijowska.json")
# send_request("../input_data/data_kijowska_smol.json")
