import json


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


def fill_data(input_data_path: str, minizinc_data, scaling: int):
    """Fills MiniZinc data file with values from given json file"""

    f = open(input_data_path)
    json_data = json.load(f)
    variables = {"time_units_in_minute": "int",
                 "number_of_time_units": "int",
                 "number_of_lights": "int",
                 # "lights": "array",
                 "number_of_roads": "int",
                 "number_of_connections": "int",
                 "car_flow_per_min": "array",
                 "roads_connections": "array2d",
                 "lights_heavy_conflicts": "array2d",
                 "heavy_conflicts_no": "int",
                 "lights_light_conflicts": "array2d",
                 "light_conflicts_no": "int"}

    for key in variables.keys():
        if key in json_data:
            if key == "number_of_time_units":
                minizinc_data.add_variable(key, json_data[key] // scaling, variables[key])
            else:
                minizinc_data.add_variable(key, json_data[key], variables[key])
        else:
            raise Exception(key + " is missing in input json file")

    f.close()
