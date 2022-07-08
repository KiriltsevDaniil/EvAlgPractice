from evpy.algorithms.base.algorithm_base import AlgorithmBase
from evpy.commands.genetic_operators.wrappers.facade.kernel import Kernel


# Algorithm parent class, defines evaluate() function signature. Used to inherit classical algorithms
class Algorithm(AlgorithmBase):
    def __init__(self, kernel: Kernel, fitness, pop_size, gen_len):
        super().__init__(kernel, fitness)

        self.pop_size = pop_size
        self.gen_length = gen_len

    def evaluate(self, T=100, p_mut=.5, p_gene_mut=.5):
        pass
