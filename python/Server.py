import json
import os
from glob import glob

from flask import Flask, request

from Optimizer import Optimizer
from python.OptimizationRequest import OptimizationRequest
from python.Utils import show_refactored_output

app = Flask(__name__)

HOST, PORT = "localhost", 9091


def clear(idx: int):
    if os.path.exists(f'../minizinc/output/{idx}*.*'):
        os.remove(f'../minizinc/output/{idx}*.*')
    if os.path.exists(f'../minizinc/data/{idx}*.dzn'):
        os.remove(f'../minizinc/data/{idx}*.dzn')
    if os.path.exists(f'../input_data/{idx}*.json'):
        os.remove(f'../input_data/{idx}*.json')


def clear_all():
    fileList = glob('../minizinc/output/[0-9]*.*')
    fileList += glob('../minizinc/data/[0-9]*.dzn')
    fileList += glob('../input_data/[0-9]*.json')
    print(fileList)
    for filePath in fileList:
        if os.path.exists(filePath):
            os.remove(filePath)


basic_optimizer = Optimizer("../minizinc/models/basic_optimizer.mzn")
improve_optimizer = Optimizer("../minizinc/models/improve_optimizer.mzn", "_i")


@app.route('/optimization', methods=['POST'])
def process_request():
    optimization_request = OptimizationRequest(request.get_json(), 3)
    optimization_request.save_as_dzn()

    try:
        basic_optimizer.solve(optimization_request)
        # improve_optimizer.solve(idx, seconds_limit=0)
        # clear(idx)
        with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
            data = json.load(f)
    except Exception as error:
        print(error)
        return json.dumps({"error_message": "Error occurred during optimization. Possibly invalid data."}), 500

    show_refactored_output(optimization_request)

    return data, 200


clear_all()
# serve(app, host=HOST, port=PORT)
app.run(host=HOST, port=PORT)
