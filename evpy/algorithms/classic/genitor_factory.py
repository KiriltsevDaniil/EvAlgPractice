from evpy.algorithms.classic.Genitor import make_genitor
from evpy.wrappers.decorators.command_list import CommandList
from evpy.algorithms.base.classic_factory import ClassicFactory


class GenitorFactory(ClassicFactory):
    def __init__(self, algorithm_builder: callable = make_genitor, supported_commands: CommandList = None):
        super().__init__(algorithm_builder, supported_commands)

    def build_genitor(self, mutator: str, recombinator: str, fitness_function: callable, pop_size: int = 5,
                      gen_len: int =10):

        if not self._check_operator(mutator):
            raise ValueError(f"Mutation function: {mutator} not found!")

        if not self._check_operator(recombinator):
            raise ValueError(f"Recombination function {recombinator} not found!")

        commands = {"mutation": mutator,
                    "recombination": recombinator,
                    "population_selector": None,
                    "parent_selector": "random_couple"}

        return self._build_algorithm(commands, fitness_function, pop_size, gen_len)
