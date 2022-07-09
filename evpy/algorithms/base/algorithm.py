from evpy.algorithms.base.algorithm_base import AlgorithmBase
from evpy.wrappers.facade.kernel import Kernel


def make_algorithm(kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
    return Algorithm(kernel, fitness, pop_size, gen_len)


# Algorithm parent class, defines evaluate() function signature. Used to inherit classical algorithms
class Algorithm(AlgorithmBase):
    def __init__(self, kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
        super().__init__(kernel, fitness)

        self.__pop_size = pop_size
        self.__gen_length = gen_len

    def evaluate(self, T: int =100, p_mut: float =.5, p_gene_mut: float =.5):
        pass

    def _get_pop_size(self):
        return self.__pop_size

    def _get_gen_length(self):
        return self.__gen_length
