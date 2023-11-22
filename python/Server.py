import json

from flask import Flask, request

from Optimizer import Optimizer
from python.OptimizationRequest import OptimizationRequest
from python.Utils import show_refactored_output, clear

app = Flask(__name__)

HOST, PORT = "localhost", 9091



@app.route('/optimization', methods=['POST'])
def process_request():
    basic_optimizer = Optimizer("../minizinc/models/basic_optimizer_new.mzn")
    optimization_request = OptimizationRequest(request.get_json())
    optimization_request.save_as_dzn()

    try:
        basic_optimizer.solve(optimization_request, "cbc")
        # improve_optimizer.solve(idx, seconds_limit=0)
        with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
            data = json.load(f)
        clear(optimization_request.idx)
    except Exception as error:
        print(error)
        return json.dumps({"error_message": "Error occurred during optimization. Possibly invalid data."}), 500
    # print(data)
    # show_refactored_output(optimization_request)
    return data, 200


# serve(app, host=HOST, port=PORT)
if __name__ == "__main__":
    clear()
    app.run(host=HOST, port=PORT)
