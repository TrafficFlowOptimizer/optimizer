import json


def prepare_output_for_backend(file_path: str):
    f = open(file_path, "r")
    content = f.readlines()

    data = {}
    results = []
    data["status"] = "success!"
    flows = list(map(float, content[-2].split(" ")))
    for i, line in enumerate(content[:-2]):
        int_array = list(map(int, line[:-2].split(" ")))
        light = {"lightId": int_array[0], "sequence": int_array[1:], "flow": flows[i]}
        results.append(light)
    data["results"] = results
    f.close()
    return data


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


def fill_data(input_data_path: str, data_path: str, scaling: int):
    """Fills MiniZinc data file with values from given json file"""

    try:
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
                    add_variable(data_path, key, json_data[key] // scaling, variables[key])
                else:
                    add_variable(data_path, key, json_data[key], variables[key])
            else:
                raise Exception(key + " is missing in input json file")

        f.close()
    except FileNotFoundError:
        print(f'{input_data_path} not found!')
