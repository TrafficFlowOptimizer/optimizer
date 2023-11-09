import json
from datetime import timedelta

from minizinc import Instance, Model, Solver

from python.OptimizationRequest import OptimizationRequest
from python.Utils import parse_solver_result


class Optimizer:
    def __init__(self, model_path: str):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""
        self.model = Model(model_path)

    def solve(self, optimization_request: OptimizationRequest, solver: str):
        """Solves problem and saves output in file on given path"""
        print(optimization_request.scaling)
        minizinc_data_path = f'../minizinc/data/{optimization_request.idx}.dzn'
        result_path = f'../minizinc/output/{optimization_request.idx}.json'

        self.model.add_file(minizinc_data_path)
        instance = Instance(Solver.lookup(solver), self.model)

        result = instance.solve(timeout=timedelta(seconds=optimization_request.optimization_time), optimisation_level=2)
        result = parse_solver_result(result, optimization_request.scaling)
        with open(result_path, 'w', encoding="utf-8") as output_txt:
            output_txt.write(json.dumps(result))
