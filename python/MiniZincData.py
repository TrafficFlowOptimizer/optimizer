class MiniZincData:
    def __init__(self, path: str):
        """Creates a new MiniZinc data file"""
        self.file_name = path
        open(self.file_name, "w").close()

    def add_variable(self, variable_name: str, variable_value, variable_type: str):
        """Adds variable\n
        It has to be one of { int, array, array2d, set of int range, set of int}"""

        file = open(self.file_name, "a")
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
        elif variable_type=="set of int range":
            file.write(str(variable_name) + " = 1.." + str(variable_value) + ";\n")
        elif variable_type=="set of int":
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

    def show(self):
        """Shows content of the MiniZinc input_data file"""

        file = open(self.file_name, "r")
        print(file.read())
        file.close()
