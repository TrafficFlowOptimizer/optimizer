from MiniZincModel import MiniZincModel


class Optimizer:
    def __init__(self, model_path: str, extension: str = ""):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""

        self.model_basic = MiniZincModel(model_path)
        self.solver_output = None
        self.input_data_path = None
        self.extension = extension

    def solve(self, optimization_request):
        """Solves problem and saves output in file on given path"""
        # open(f'../minizinc/output/{idx}{self.extension}.txt', "w")

        variables = {"time_units_in_minute": "int",
                     "number_of_time_units": "int",
                     "lights_count": "int",
                     "roads_count": "int",
                     "connections_count": "int",
                     "car_flow_per_minute": "array",
                     "roads_connections": "array2d",
                     "heavy_collisions": "array2d",
                     "heavy_collisions_count": "int",
                     "light_collisions": "array2d",
                     "light_collisions_count": "int"}

        # if self.extension=="_b":
        #     fill_data(f'../input_data/{idx}.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)
        # else:
        #     fill_data(f'../input_data/{idx}.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)
        #     variables["results"] = "array2d"
        #     fill_data(f'../minizinc/output/{idx}_b.json', f'../minizinc/data/{idx}{self.extension}.dzn', variables, scaling)
        self.model_basic.solve(f'../minizinc/data/{optimization_request.idx}{self.extension}.dzn',
                               f'../minizinc/output/{optimization_request.idx}{self.extension}.json',
                               "cbc", optimization_request)

        # if self.extension == "_i":
        #     with open(f'../minizinc/output/{idx}{self.extension}.json', 'r+') as f:
        #         content = json.load(f)
        #         pprint(content)
        #         result = content["results"]
        #         extended_sequence = []
        #         for sequence in result:
        #             extended_sequence.append([])
        #             for s in sequence:
        #                 for i in range(scaling):
        #                     extended_sequence[-1].append(s)
        #         print(extended_sequence)
        #         content["results"] = extended_sequence
        #         # for result in content["results"]:
        #         #     extended_sequence = []
        #         #     for q in result["sequence"]:
        #         #         for i in range(scaling):
        #         #             extended_sequence.append(q)
        #         #     result["sequence"] = extended_sequence
        #         #     result["flow"] = round(result["flow"] * scaling, 4)
        #         # content["status"] = "success!"
        #
        #         with open(f'../minizinc/output/{idx}{self.extension}.json', "w") as jsonFile:
        #             json.dump(content, jsonFile)

    def show_model(self):
        """Shows content of the MiniZinc model"""
        self.model_basic.show()
