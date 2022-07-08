from evpy.algorithms.base.algorithm_base import make_base
from evpy.commands.genetic_operators.wrappers.facade.kernel_factory import KernelFactory
from evpy.commands.genetic_operators.wrappers.decorators.command_list import CommandList


class BaseFactory:
    def __init__(self, builder=make_base, supported_commands=None):

        if not supported_commands:
            self.__supported = CommandList()
        else:
            self.__supported = supported_commands

        self.__builder = builder
        self.__supplier = KernelFactory()

    def build_algorithm(self, fitness_function, algorithm: dict):
        _kernel = self.__supplier.build_kernel(self.__supported.get_command(algorithm["mutation"]),
                                               self.__supported.get_command(algorithm["recombination"]),
                                               self.__supported.get_command(algorithm["population_selector"]),
                                               self.__supported.get_command(algorithm["parent_selector"]))

        return self.__builder(_kernel, fitness_function)
