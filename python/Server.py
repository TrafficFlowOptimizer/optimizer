import json

from flask import Flask, request

from Optimizer import Optimizer
from python.OptimizationRequest import OptimizationRequest
from python.Utils import show_refactored_output, clear

app = Flask(__name__)

HOST, PORT = "localhost", 9091

basic_optimizer = Optimizer("../minizinc/models/basic_optimizer_new.mzn")


# improve_optimizer = Optimizer("../minizinc/models/improve_optimizer.mzn", "_i")


@app.route('/optimization', methods=['POST'])
def process_request():
    optimization_request = OptimizationRequest(request.get_json(), 3)
    optimization_request.save_as_dzn()

    try:
        basic_optimizer.solve(optimization_request, "cbc")
        # improve_optimizer.solve(idx, seconds_limit=0)
        # clear(idx)
        with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
            data = json.load(f)
    except Exception as error:
        print(error)
        return json.dumps({"error_message": "Error occurred during optimization. Possibly invalid data."}), 500

    show_refactored_output(optimization_request)

    return data, 200


clear()
# serve(app, host=HOST, port=PORT)
app.run(host=HOST, port=PORT)
