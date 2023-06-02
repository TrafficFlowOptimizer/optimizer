from datetime import timedelta
from pprint import pprint

from MiniZincModel import MiniZincModel
from Utils import *


class Optimizer:
    def __init__(self, model_path: str, extension: str):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""

        self.model_basic = MiniZincModel(model_path)
        self.solver_output = None
        self.input_data_path = None
        self.extension = extension

    def solve(self, idx: int, scaling: int = 3, seconds_limit=60):
        """Solves problem and saves output in file on given path"""
        open(f'../minizinc/data/{idx}{self.extension}.dzn', "w")

        variables = {"time_units_in_minute": "int",
                     "number_of_time_units": "int",
                     "number_of_lights": "int",
                     "number_of_roads": "int",
                     "number_of_connections": "int",
                     "car_flow_per_min": "array",
                     "roads_connections": "array2d",
                     "lights_heavy_collisions": "array2d",
                     "heavy_collisions_no": "int",
                     "lights_light_collisions": "array2d",
                     "light_collisions_no": "int"}

        if self.extension=="_b":
            fill_data(f'../input_data/{idx}.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)
        else:
            fill_data(f'../input_data/{idx}.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)
            variables["results"] = "array2d"
            fill_data(f'../minizinc/output/{idx}_b.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)

        if seconds_limit == -1:
            self.model_basic.solve(f'../minizinc/data/{idx}{self.extension}.dzn',
                                   f'../minizinc/output/{idx}{self.extension}.json', "cbc")
        else:
            self.model_basic.solve(f'../minizinc/data/{idx}{self.extension}.dzn',
                                   f'../minizinc/output/{idx}{self.extension}.json', "cbc",
                                   timedelta(seconds=seconds_limit))

        if self.extension == "_i":
            with open(f'../minizinc/output/{idx}{self.extension}.json', 'r+') as f:
                content = json.load(f)
                pprint(content)
                result = content["results"]
                extended_sequence = []
                for sequence in result:
                    extended_sequence.append([])
                    for s in sequence:
                        for i in range(scaling):
                            extended_sequence[-1].append(s)
                print(extended_sequence)
                content["results"] = extended_sequence
                # for result in content["results"]:
                #     extended_sequence = []
                #     for q in result["sequence"]:
                #         for i in range(scaling):
                #             extended_sequence.append(q)
                #     result["sequence"] = extended_sequence
                #     result["flow"] = round(result["flow"] * scaling, 4)
                # content["status"] = "success!"

                with open(f'../minizinc/output/{idx}{self.extension}.json', "w") as jsonFile:
                    json.dump(content, jsonFile)

    def show_model(self):
        """Shows content of the MiniZinc model"""
        self.model_basic.show()
