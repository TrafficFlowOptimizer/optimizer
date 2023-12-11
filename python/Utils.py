import os
from glob import glob


def add_variable(file_name: str, variable_name: str, variable_value, variable_type: str):
    """Adds variable\n
    It has to be one of { int, array, array2d, set of int range, set of int}"""

    file = open(file_name, "a")
    if variable_type in ["int", "array", "1darray"]:
        file.write(str(variable_name) + " = " + str(variable_value) + ";\n")
    elif variable_type == "array2d":
        if str(variable_value) == "[]":
            value = "[]"
        else:
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


def parse_solver_result(result: list[list[int]], scaling: int):
    extended_lights = []
    for light_seq in result:
        extended_light_seq = []
        for light in light_seq:
            for _ in range(scaling):
                extended_light_seq.append(light)
        extended_lights.append(extended_light_seq)
    return extended_lights


def clear(idx: int = None):
    try:
        if idx is None:
            fileList = glob('../minizinc/data/[0-9]*.dzn')
        else:
            fileList = glob(f'../minizinc/data/{idx}*.dzn')
        for filePath in fileList:
            if os.path.exists(filePath):
                os.remove(filePath)
    except Exception:
        pass
