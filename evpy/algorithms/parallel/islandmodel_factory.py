from evpy.algorithms.parallel.IslandModel import make_island_model
from evpy.algorithms.base.parallel_factory import ParallelFactory
from evpy.algorithms.classic.canonical_factory import CanonicalFactory
from evpy.algorithms.classic.genitor_factory import GenitorFactory


class IslandModelFactory(ParallelFactory):
    def __init__(self, builder: callable = None):
        if builder is None:
            builder = make_island_model

        super().__init__(builder)
        self.canon = CanonicalFactory()
        self.genitor = GenitorFactory()

    def make_island_model(self, parameters: list[list], fitness_function: callable, gen_len: int,
                          rule: callable = None):

        algorithm_parameters = self.generate_arguments(parameters, fitness_function, gen_len)

        archipelago = []

        for parameter in algorithm_parameters:
            if len(parameter) > 3:
                archipelago.append(self.genitor.build_genitor(**parameter))
            else:
                archipelago.append(self.canon.build_canonical(**parameter))

        return self.builder(archipelago, fitness_function, rule)

    @staticmethod
    def generate_arguments(parameters: list[list], fitness: callable, gen_len: int):
        arguments = []

        for parameter in parameters:
            if len(parameter) > 3:
                arguments.append({
                    "fitness_function": fitness,
                    "gen_len": gen_len,
                    "pop_size": parameter[0],
                    "mutator": parameter[1],
                    "recombinator": parameter[2]
                })
            else:
                arguments.append({
                    "fitness_function": fitness,
                    "gen_len": gen_len,
                    "pop_size": parameter[0],
                })

            return arguments
