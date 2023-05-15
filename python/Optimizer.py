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

        if seconds_limit is None:
            self.model_basic.solve(f'../minizinc/data/{idx}.dzn', f'../minizinc/output/{idx}.txt', "cbc")
        else:
            self.model_basic.solve(f'../minizinc/data/{idx}.dzn', f'../minizinc/output/{idx}.txt', "cbc",
                                   timedelta(seconds=seconds_limit))

    def show_data(self, idx: int):
        """Shows content of the MiniZinc data file"""
        file = open(f'../minizinc/data/{idx}.dzn', "r")
        print(file.read())
        file.close()

    def show_model(self):
        """Shows content of the MiniZinc model"""
        self.model_basic.show()

    def show_raw_output(self, idx: int):
        """Shows solver's raw output"""
        file = open(f'../minizinc/output/{idx}.txt', "r")
        print(file.read())
        file.close()

    def show_refactored_output(self, idx: int, scaling: int = 3):
        """Shows refactored MinZinc output so it is easier to read"""
        output = get_output_lights(f'../minizinc/output/{idx}.txt')
        lights_types = get_value_from_input(f'../input_data/{idx}.json', "lights_type")
        car_flow_per_min = get_value_from_input(f'../input_data/{idx}.json', "car_flow_per_min")

        for light in range(1, len(output[0])):
            print("ID: ", '{:0>2}'.format(light - 1), ";", lights_types[light - 1], sep="", end=";")
            for time in range(len(output) - 2):
                if output[time][light] == "1":
                    # if (light - 1) % 3 == 2 and output[time][light - 1] != "1":
                    #     print(">" * scaling, end="")
                    # else:
                    print("O" * scaling, end="")
                elif output[time][light] == "0":
                    print("_" * scaling, end="")
                else:
                    print("*" * scaling, end="")
            print(end=";")
            print("car flow: ", '{:0>2}'.format(car_flow_per_min[light - 1]), "/min", sep="", end="; ")
            print("ratio: ", '{:.2f}'.format(float(output[-2][light - 1]) * scaling), sep="")
        print("Minimum flow: ", '{:.4f}'.format(float(output[-1][0]) * scaling), sep="")

# def test_times(scaling: int = 2, time_limit=None):
#     optimizer = Optimizer("../input_data/data_kijowska.json", "../minizinc/output/output.txt", scaling)
#     timer = time.time()
#     optimizer.solve(time_limit)
#     timer = time.time() - timer
#     optimizer.show_refactored_output(scaling)
#     print('{:.3f}'.format(timer), "seconds, ", end="")
#     if time_limit is not None and timer > time_limit:
#         print("optimization aborted due to time limit.")
#     else:
#         print("best solution found.")
#
#
# test_times(3, 30)  # 58.182
# test_times(2, 30)  # 404.534
# test_times(1, 30)  # 7271.367
