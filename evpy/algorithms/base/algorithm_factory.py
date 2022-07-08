from evpy.algorithms.base.algorithm import make_algorithm
from evpy.commands.genetic_operators.wrappers.decorators.command_list import CommandList
from evpy.commands.genetic_operators.wrappers.facade.kernel_factory import KernelFactory


class AlgorithmFactory:
    def __init__(self, builder=make_algorithm, supported_commands=None):

        if not supported_commands:
            self.__supported = CommandList()
        else:
            self.__supported = supported_commands

        self.__supplier = KernelFactory()
        self.__builder = builder

    def build_algorithm(self, algorithm: dict, fitness_function, pop_size: int, gen_len: int):
        _kernel = self.__supplier.build_kernel(self.__supported.get_command(algorithm["mutation"]),
                                               self.__supported.get_command(algorithm["recombination"]),
                                               self.__supported.get_command(algorithm["population_selector"]),
                                               self.__supported.get_command(algorithm["parent_selector"]))

        return self.__builder(_kernel, fitness_function, pop_size, gen_len)


def a():
    return -1


alg_fac = AlgorithmFactory()
alg = alg_fac.build_algorithm({"mutation": "point_mutation",
                               "recombination": "single_point_crossover",
                               "population_selector": "elite_selection",
                               "parent_selector": "random_couple"}, a, 10, 4)


