import os
from datetime import timedelta
from glob import glob

from minizinc import Instance, Model, Solver

from OptimizationRequest import OptimizationRequest
from Utils import parse_solver_result


class Optimizer:
    def __init__(self, model_path: str, model_model_for_comparison_path: str):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""
        self.model = Model(model_path)
        self.model_for_comparison = Model(model_model_for_comparison_path)
        self.DEFAULT_SOLVER = os.getenv('DEFAULT_SOLVER')

    def solve(self, optimization_request: OptimizationRequest, solver_name: str):
        """Solves problem and returns best result"""
        minizinc_data_path = f'../minizinc/data/{optimization_request.idx}.dzn'

        self.model.add_file(minizinc_data_path)

        try:
            solver = Solver.lookup(solver_name, refresh=True)
        except LookupError:
            solver = Solver.lookup(self.DEFAULT_SOLVER, refresh=True)

        instance = Instance(solver, self.model)

        result = instance.solve(timeout=timedelta(seconds=optimization_request.optimization_time),
                                optimisation_level=2, intermediate_solutions=True)

        previous_objective = self.calculate_previous_objective(optimization_request, solver)
        current_objective = result.objective

        if len(result) == 0:
            return None
        if previous_objective > current_objective:
            return optimization_request.previous_results

        return parse_solver_result(result.solution[-1].is_light_on, optimization_request.scaling)

    def calculate_previous_objective(self, optimization_request: OptimizationRequest, solver: Solver):
        minizinc_data_path = glob(f'../minizinc/data/{optimization_request.idx}_for_comparison.dzn')
        if len(minizinc_data_path) == 0:
            return 0

        self.model_for_comparison.add_file(minizinc_data_path[0])
        instance = Instance(solver, self.model_for_comparison)

        result = instance.solve(optimisation_level=2)
        return result.objective / optimization_request.scaling
