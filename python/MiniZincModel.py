from datetime import timedelta

from minizinc import Instance, Model, Solver
import asyncio

class MiniZincModel:
    def __init__(self, path: str):
        """Creates a new or opens existing MiniZinc model"""
        self.file_name = path
        open(self.file_name, "a").close()

    def solve(self, data_path: str, output_name: str, solver: str, time_limit: timedelta = None):
        """Solves problem with given solver and saves output to the given file"""
        model = Model(self.file_name)
        coin_or = Solver.lookup(solver)
        # instance.add_file(self.data_file_name)
        model.add_file(data_path)
        instance = Instance(coin_or, model)

        result = instance.solve(timeout=time_limit, optimisation_level=2)
        print("printing")
        print(result)
        with open(output_name, 'w', encoding="utf-8") as output_txt:
            output_txt.write(str(result))

        # task = asyncio.create_task(instance.solve_async(timeout=time_limit, optimisation_level=2))
        # done, pending = await asyncio.wait([task], return_when=asyncio.FIRST_COMPLETED)
        # for p in pending:
        #     p.cancel()
        # for t in done:
        #     print(t.result())
        #     with open(output_name, 'w', encoding="utf-8") as output_txt:
        #         output_txt.write(str(t.result()))

    def show(self):
        """Shows content of the MiniZinc model"""

        file = open(self.file_name, "r")
        print(file.read())
        file.close()
