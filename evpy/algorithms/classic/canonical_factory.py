from evpy.algorithms.classic.Canonical import make_canonical
from evpy.wrappers.decorators.command_list import CommandList
from evpy.algorithms.base.classic_factory import ClassicFactory


class CanonicalFactory(ClassicFactory):
    def __init__(self, algorithm_builder: callable = make_canonical, supported_commands: CommandList = None):
        super().__init__(algorithm_builder, supported_commands)

    def build_canonical(self, fitness_function: callable, pop_size: int = 5, gen_len: int = 10):
        commands = {"mutation": "point_mutation",
                    "recombination": "single_point_crossover",
                    "population_selector": None,
                    "parent_selector": "fitness_proportional_selection"}

        return self._build_algorithm(commands, fitness_function, pop_size, gen_len)
