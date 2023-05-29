from datetime import timedelta

from MiniZincModel import MiniZincModel
from Utils import *


class Optimizer:
    def __init__(self):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""

        self.model_basic = MiniZincModel("../minizinc/models/optimizer.mzn")
        self.solver_output = None
        self.input_data_path = None

    def solve(self, idx: int, scaling: int = 3, seconds_limit=60):
        """Solves problem and saves output in file on given path"""
        open(f'../minizinc/data/{idx}.dzn', "w")

        fill_data(f'../input_data/{idx}.json', f'../minizinc/data/{idx}.dzn', scaling)

        if seconds_limit == -1:
            self.model_basic.solve(f'../minizinc/data/{idx}.dzn', f'../minizinc/output/{idx}.json', "cbc")
        else:
            self.model_basic.solve(f'../minizinc/data/{idx}.dzn', f'../minizinc/output/{idx}.json', "cbc",
                                   timedelta(seconds=seconds_limit))

        with open(f'../minizinc/output/{idx}.json', 'r+') as f:
            content = json.load(f)
            for result in content["results"]:
                extended_sequence = []
                for q in result["sequence"]:
                    for i in range(scaling):
                        extended_sequence.append(q)
                result["sequence"] = extended_sequence
                result["flow"] = round(result["flow"] * scaling, 4)
            content["status"] = "success!"

        with open(f'../minizinc/output/{idx}.json', "w") as jsonFile:
            json.dump(content, jsonFile)

    def show_model(self):
        """Shows content of the MiniZinc model"""
        self.model_basic.show()
