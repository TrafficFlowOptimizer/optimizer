import json

from flask import Flask, request
from dotenv import load_dotenv
import os
from Optimizer import Optimizer
from OptimizationRequest import OptimizationRequest
from Utils import show_refactored_output, clear

app = Flask(__name__)

load_dotenv("../.env")

# server info
SERVER_HOST = os.getenv('SPRING_HOST')
SERVER_PORT = os.getenv('SPRING_PORT')
SERVER = "http://" + SERVER_HOST + ":" + SERVER_PORT + "/"

# OT setup
HOST, PORT = os.getenv('OT_HOST'), int(os.getenv('OT_PORT'))
SOLVER = os.getenv('SOLVER')



@app.route('/', methods=['GET'])
def hi():
    return "OK", 200

@app.route('/optimization', methods=['POST'])
def process_request():
    basic_optimizer = Optimizer("../minizinc/models/basic_optimizer_new.mzn")
    optimization_request = OptimizationRequest(request.get_json())
    optimization_request.save_as_dzn()

    try:
        basic_optimizer.solve(optimization_request, SOLVER)
        show_refactored_output(optimization_request)
        # improve_optimizer.solve(idx, seconds_limit=0)
        with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
            data = json.load(f)
        clear(optimization_request.idx)
    except Exception as error:
        print(error)
        return json.dumps({"error_message": "Error occurred during optimization. Possibly invalid data."}), 500
    # print(data)
    return data, 200


# serve(app, host=HOST, port=PORT)
if __name__ == "__main__":
    clear()
    app.run(host="0.0.0.0", port=PORT)
