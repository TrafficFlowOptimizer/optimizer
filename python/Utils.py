import json
from warnings import warn

from minizinc import Result


def get_value_from_input(input_data_path: str, value_name: str):
    """Returns given data from input json file"""
    f = open(input_data_path)
    json_data = json.load(f)
    result = json_data[value_name]
    f.close()
    return result


def get_output_lights(file_path: str):
    """Returns lights sequence from solver output file"""
    file = open(file_path, "r")
    lines = file.readlines()
    output = []
    for line in lines:
        output.append(line.split())
    file.close()
    return output


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
    # elif variable_type=="3darray":
    #     file.write(str(variable_name) + " = " + str(variable_value) + ";\n")
    else:
        raise ValueError("Invalid \"variable_type\" for " + str(variable_name) + ": " + str(variable_type))
    file.close()


def fill_data(input_data_path: str, data_path: str, variables: dict, scaling: int):
    """Fills MiniZinc data file with values from given json file"""

    try:
        f = open(input_data_path)
        json_data = json.load(f)

        for key in variables.keys():
            if key in json_data:
                if key == "number_of_time_units":
                    add_variable(data_path, key, json_data[key] // scaling, variables[key])
                else:
                    add_variable(data_path, key, json_data[key], variables[key])
            else:
                warn(key + " is missing in input json file")

        f.close()
    except FileNotFoundError:
        print(f'{input_data_path} not found!')


def show_data(idx: int, extension: str):
    """Shows content of the MiniZinc data file"""
    file = open(f'../minizinc/data/{idx}{extension}.dzn', "r")
    print(file.read())
    file.close()


def show_raw_output(idx: int, extension: str):
    """Shows solver's raw output"""
    file = open(f'../minizinc/output/{idx}{extension}.txt', "r")
    print(file.read())
    file.close()


def parse_solver_result(result: Result, scaling: int):
    parsed_result = {}
    for light_id, light_seq in enumerate(json.loads(str(result))["results"]):
        extended_light_seq = []
        for light in light_seq:
            for _ in range(scaling):
                extended_light_seq.append(light)
        parsed_result[light_id] = extended_light_seq
    return parsed_result


def show_refactored_output(optimization_request):
    """Shows refactored MinZinc output so it is easier to read"""
    with open(f'../minizinc/output/{optimization_request.idx}.json', 'r+') as f:
        result = json.load(f)

    lights_types = optimization_request.lights_type
    car_flow_per_minute = optimization_request.car_flow_per_minute

    for light_id, light_seq in result.items():
        print("ID: ", '{:0>2}'.format(int(light_id)), ";", lights_types[int(light_id)], sep="", end=";")
        for light in light_seq:
            if light == 1:
                print("O", end="")
            elif light == 0:
                print("_", end="")
            else:
                print("*", end="")
        print(end=";")
        print("car flow: ", '{:0>2}'.format(car_flow_per_minute[int(light_id)]), "/min", sep="")
