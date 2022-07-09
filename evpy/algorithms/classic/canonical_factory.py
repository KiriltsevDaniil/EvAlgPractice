from evpy.algorithms.classic.Canonical import make_canonical
from evpy.algorithms.base.algorithm_factory import AlgorithmFactory


class CanonicalFactory(AlgorithmFactory):
    def __init__(self, algorithm_builder=make_canonical, supported_commands=None):
        super().__init__(algorithm_builder, supported_commands)

    def build_canonical(self, fitness_function, pop_size=5, gen_len=10):
        commands = {"mutation": "point_mutation",
                    "recombination": "single_point_crossover",
                    "population_selector": None,
                    "parent_selector": "fitness_proportional_selection"}

        return self._build_algorithm(commands, fitness_function, pop_size, gen_len)
