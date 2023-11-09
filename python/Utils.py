import json
import os
from glob import glob

from minizinc import Result


def add_variable(file_name: str, variable_name: str, variable_value, variable_type: str):
    """Adds variable\n
    It has to be one of { int, array, array2d, set of int range, set of int}"""

    file = open(file_name, "a")
    if variable_type in ["int", "array", "1darray"]:
        file.write(str(variable_name) + " = " + str(variable_value) + ";\n")
    elif variable_type == "array2d":
        inline_size = len(variable_name) + 4
        inline = " " * inline_size
        value = "["
        for row in variable_value:
            value += "| "
            for v in row:
                value += str(v) + ", "
            value += "\n" + inline
        value = value[:-3 - inline_size] + " |]"
        file.write(str(variable_name) + " = " + value + ";\n")
    elif variable_type == "set of int range":
        file.write(str(variable_name) + " = 1.." + str(variable_value) + ";\n")
    elif variable_type == "set of int":
        value = "{"
        for v in variable_value:
            value += str(v) + ", "
        value = value[:-2] + "}"
        file.write(str(variable_name) + " = " + value + ";\n")
    elif variable_type == "3darray":
        file.write(str(variable_name) + " = " + str(variable_value) + ";\n")
    else:
        raise ValueError("Invalid \"variable_type\" for " + str(variable_name) + ": " + str(variable_type))
    file.close()


def parse_solver_result(result: Result, scaling: int):
    parsed_result = {}
    result_json = json.loads(str(result))
    lights = {}
    for light_id, light_seq in enumerate(result_json["results"]):
        extended_light_seq = []
        for light in light_seq:
            for _ in range(scaling):
                extended_light_seq.append(light)
        lights[light_id+1] = extended_light_seq
    parsed_result["lights_sequences"] = lights
    parsed_result["car_flows_current"] = [flow*scaling for flow in result_json["car_flows_current"]]
    parsed_result["car_flows_expected"] = result_json["car_flows_expected"]
    return parsed_result


def show_refactored_output(optimization_request):
    """Shows refactored MinZinc output so it is easier to read"""
    with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
        result = json.load(f)

    lights_types = optimization_request.lights_type

    for light_id, light_seq in result["lights_sequences"].items():
        print("LightID: ", '{:0>2}'.format(int(light_id)), ";", lights_types[int(light_id)-1], sep="", end=";")
        for light in light_seq:
            if light == 1:
                print("O", end="")
            elif light == 0:
                print("_", end="")
            else:
                print("*", end="")
        print()
    print("Current/expected flow per minute:")
    average_ratio = 0
    for connection_id in range(len(result["car_flows_expected"])):
        average_ratio += result["car_flows_current"][connection_id]/result["car_flows_expected"][connection_id]
        print("Connection: ", '{:0>2}'.format(int(connection_id)+1), "; ",
              '{:.2f}'.format(result["car_flows_current"][connection_id]/result["car_flows_expected"][connection_id]),
              f' ({result["car_flows_current"][connection_id]} / {result["car_flows_expected"][connection_id]})', sep="")
    average_ratio /= len(result["car_flows_expected"])
    print("Average ratio:", '{:.2f}'.format(average_ratio))

def clear(idx: int = None):
    if idx is None:
        fileList = glob('../minizinc/output/[0-9]*.*')
        fileList += glob('../minizinc/data/[0-9]*.dzn')
        fileList += glob('../input_data/[0-9]*.json')
    else:
        fileList = glob(f'../minizinc/output/{idx}.*')
        fileList += glob(f'../minizinc/data/{idx}.dzn')
        fileList += glob(f'../input_data/{idx}.json')
    for filePath in fileList:
        if os.path.exists(filePath):
            os.remove(filePath)
