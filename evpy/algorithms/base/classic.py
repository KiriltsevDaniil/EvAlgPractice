from evpy.algorithms.base.algorithm import Algorithm
from evpy.wrappers.facade.kernel import Kernel


def make_classic(kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
    return Classic(kernel, fitness, pop_size, gen_len)


# Algorithm parent class, defines evaluate() function signature. Used to inherit classical algorithms
class Classic(Algorithm):
    def __init__(self, kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
        super().__init__(fitness)

        self.__kernel = kernel
        self.__pop_size = pop_size
        self.__gen_length = gen_len

        self.__current_population = None

    def evaluate(self, T: int =100, p_mut: float =.5, p_gene_mut: float =.5):
        pass

    def _get_pop_size(self):
        return self.__pop_size

    def _get_gen_length(self):
        return self.__gen_length

    def _get_kernel(self):
        return self.__kernel

    def _get_current(self):
        return self.__current_population

    def _set_current(self, value: list):
        self.__current_population = value
