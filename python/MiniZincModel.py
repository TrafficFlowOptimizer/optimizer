from datetime import timedelta

from minizinc import Instance, Model, Solver


class MiniZincModel:
    def __init__(self, path: str):
        """Creates a new or opens existing MiniZinc model"""
        self.file_name = path
        open(self.file_name, "a").close()

    def solve(self, data_path: str, output_name: str, solver: str, time_limit: timedelta = None):
        """Solves problem with given solver and saves output to the given file"""
        model = Model(self.file_name)
        coin_or = Solver.lookup(solver)
        model.add_file(data_path)
        instance = Instance(coin_or, model)

        result = instance.solve(timeout=time_limit, optimisation_level=2)
        with open(output_name, 'w', encoding="utf-8") as output_txt:
            output_txt.write(str(result))

    def show(self):
        """Shows content of the MiniZinc model"""

        file = open(self.file_name, "r")
        print(file.read())
        file.close()
