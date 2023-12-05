from datetime import timedelta

from minizinc import Instance, Model, Solver

from OptimizationRequest import OptimizationRequest
from Utils import parse_solver_result


class Optimizer:
    def __init__(self, model_path: str):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""
        self.model = Model(model_path)

    def solve(self, optimization_request: OptimizationRequest, solver: str):
        """Solves problem and saves output in file on given path"""
        minizinc_data_path = f'../minizinc/data/{optimization_request.idx}.dzn'
        result_path = f'../minizinc/output/{optimization_request.idx}.json'

        self.model.add_file(minizinc_data_path)
        instance = Instance(Solver.lookup(solver, refresh=True), self.model)

        result = instance.solve(timeout=timedelta(seconds=optimization_request.optimization_time),
                                optimisation_level=2, intermediate_solutions=True)

        if len(result) == 0:
            return None
        print(result.solution[-1].is_light_on)
        print(result.solution[-1].is_light_on[0])
        return parse_solver_result(result.solution[-1].is_light_on, optimization_request.scaling)
