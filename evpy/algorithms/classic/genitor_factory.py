from evpy.algorithms.classic.Genitor import make_genitor
from evpy.algorithms.base.algorithm_factory import AlgorithmFactory


class GenitorFactory(AlgorithmFactory):
    def __init__(self, algorithm_builder=make_genitor, supported_commands=None):
        super().__init__(algorithm_builder, supported_commands)

    def build_genitor(self, mutator: str, recombinator: str, fitness_function, pop_size=5, gen_len=10):

        if not self._check_operator(mutator):
            raise ValueError(f"Mutation function: {mutator} not found!")

        if not self._check_operator(recombinator):
            raise ValueError(f"Recombination function {recombinator} not found!")

        commands = {"mutation": mutator,
                    "recombination": recombinator,
                    "population_selector": None,
                    "parent_selector": "random_couple"}

        return self._build_algorithm(commands, fitness_function, pop_size, gen_len)
