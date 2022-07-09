from evpy.algorithms.base.algorithm import make_algorithm
from evpy.wrappers.decorators.command_list import CommandList
from evpy.wrappers.facade.kernel_factory import KernelFactory


class AlgorithmFactory:
    def __init__(self, algorithm_builder: callable = None, kernel_builder: callable = None,
                 command_builder: callable = None, supported_commands=None):

        if not supported_commands:
            self.__supported = CommandList()
        else:
            self.__supported = supported_commands

        if not algorithm_builder:
            algorithm_builder = make_algorithm

        self.__supplier = KernelFactory(kernel_builder, command_builder)
        self.__builder = algorithm_builder

    def _build_algorithm(self, algorithm: dict, fitness_function, pop_size: int, gen_len: int):
        _kernel = self.__supplier.build_kernel(
            self.__supported.get_command(algorithm["mutation"]) if algorithm["mutation"] else None,
            self.__supported.get_command(algorithm["recombination"]) if algorithm["recombination"] else None,
            self.__supported.get_command(algorithm["population_selector"]) if algorithm["population_selector"] else None,
            self.__supported.get_command(algorithm["parent_selector"]) if algorithm["parent_selector"] else None)

        return self.__builder(_kernel, fitness_function, pop_size, gen_len)

    def _check_operator(self, operator: str):
        return self.__supported.get_command(operator)
