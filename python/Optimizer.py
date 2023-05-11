import time
from datetime import timedelta

from MiniZincData import MiniZincData
from MiniZincModel import MiniZincModel
from Utils import *


class Optimizer:
    def __init__(self, input_data_path: str, scaling: int):
        """Creates Optimizer class with MiniZinc model and Minizinc data files on given paths"""
        self.input_data_path = input_data_path

        self.model_data = MiniZincData("../minizinc/data/data.dzn")
        fill_data(input_data_path, self.model_data, scaling)

        self.model_basic = MiniZincModel("../minizinc/models/optimizer.mzn",
                                         "../minizinc/data/data.dzn")

        self.solver_output = "../minizinc/output/output.txt"

    def solve(self, seconds_limit=60):
        """Solves problem and saves output in file on given path"""
        if seconds_limit is None:
            self.model_basic.solve(self.solver_output, "cbc")
        else:
            self.model_basic.solve(self.solver_output, "cbc", timedelta(seconds=seconds_limit))

    def show_data(self):
        """Shows content of the MiniZinc data file"""
        self.model_data.show()

    def show_model(self):
        """Shows content of the MiniZinc model"""
        self.model_data.show()

    def show_raw_output(self):
        """Shows solver's raw output"""
        file = open(self.solver_output, "r")
        print(file.read())
        file.close()

    def show_refactored_output(self, scaling: int = 3):
        """Shows refactored MinZinc output so it is easier to read"""
        output = get_output_lights(self.solver_output)
        lights_types = get_value_from_input(self.input_data_path, "lights_type")
        car_flow_per_min = get_value_from_input(self.input_data_path, "car_flow_per_min")

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


def test_times(scaling: int = 2, time_limit=None):
    optimizer = Optimizer("../input_data/data_kijowska.json", scaling)
    timer = time.time()
    optimizer.solve(time_limit)
    timer = time.time() - timer
    optimizer.show_refactored_output(scaling)
    print('{:.3f}'.format(timer), "seconds, ", end="")
    if time_limit is not None and timer > time_limit:
        print("optimization aborted due to time limit.")
    else:
        print("best solution found.")


test_times(3, 30)  # 58.182
test_times(2, 30)  # 404.534
test_times(1, 30)  # 7271.367