from evpy.algorithms.base.algorithm_base import AlgorithmBase
from evpy.commands.genetic_operators.wrappers.facade.kernel import Kernel


def make_algorithm(kernel: Kernel, fitness, pop_size: int, gen_len: int):
    return Algorithm(kernel, fitness, pop_size, gen_len)


# Algorithm parent class, defines evaluate() function signature. Used to inherit classical algorithms
class Algorithm(AlgorithmBase):
    def __init__(self, kernel: Kernel, fitness, pop_size: int, gen_len: int):
        super().__init__(kernel, fitness)

        self._pop_size = pop_size
        self.__gen_length = gen_len

    def evaluate(self, T=100, p_mut=.5, p_gene_mut=.5):
        pass
