from evpy.wrappers.facade.kernel import Kernel
from evpy.algorithms.base.algorithm import Algorithm

from random import randint, random


def make_genitor(kernel: Kernel, fitness, pop_size, gen_len):
    return Genitor(kernel, fitness, pop_size, gen_len)


class Genitor(Algorithm):
    """Genitor GA (Whitley's model)"""
    def __init__(self, kernel: Kernel, fitness, pop_size=5, gen_len=10):
        super().__init__(kernel, fitness, pop_size, gen_len)


    def evaluate(self, T=100, p_gene_mut=.5, p_mut=.5):
        t,  equilibrium = 0, False
        init_population = [[randint(0, 1) for y in range(self._get_gen_length())] for x in range(self._get_pop_size())]
        weighted_pop = [[x, self._get_fitness()(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)
        for i in range(1, len(weighted_pop)):
            if weighted_pop[i][1] != weighted_pop[i-1][1]:
                break
            if i == (len(weighted_pop) - 1) and weighted_pop[i][1] == weighted_pop[i-1][1]:
                equilibrium = True
        while not equilibrium and t < T:
            print(t)
            if self._get_fittest() is None and self._get_max_fitness() is None:
                self._set_fittest(weighted_pop[0][0])
                self._set_max_fitness(weighted_pop[0][1])
            elif weighted_pop[0][1] > self._get_max_fitness():
                self._set_fittest(weighted_pop[0][0])
                self._set_max_fitness(weighted_pop[0][1])
            self._add_to_memory([self._get_max_fitness(), t])

            parents = self._get_kernel().parent_selection(weighted_pop)
            _, children = self._get_kernel().recombination(parents[0], parents[1])
            child = children[randint(0, 1)]
            child = self._get_kernel().mutation(child, p_mut=p_gene_mut) if random() <= p_mut else child
            child = [child, self._get_fitness()(child)]
            weighted_pop[-1] = child

            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            for i in range(1, len(weighted_pop)):
                if weighted_pop[i][1] != weighted_pop[i-1][1]:
                    break
                if i == (len(weighted_pop) - 1) and weighted_pop[i][1] == weighted_pop[i-1][1]:
                    equilibrium = True
            t += 1

        if self._get_fittest() is None and self._get_max_fitness() is None:
            self._set_fittest(weighted_pop[0][0])
            self._set_max_fitness(weighted_pop[0][1])
        elif weighted_pop[0][1] > self._get_max_fitness():
            self._set_fittest(weighted_pop[0][0])
            self._set_max_fitness(weighted_pop[0][1])
        self._add_to_memory([self._get_max_fitness(), t])

        return self._get_fittest()
