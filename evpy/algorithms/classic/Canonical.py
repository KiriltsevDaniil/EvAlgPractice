from evpy.algorithms.base.algorithm import Algorithm
from evpy.commands.genetic_operators.wrappers.facade.kernel import Kernel
from random import randint, sample, random


class Canonical(Algorithm):
    """Canonical GA (Holland's model)"""
    def __init__(self, kernel: Kernel, fitness, pop_size=5, gen_len=10):
        super().__init__(kernel, fitness, pop_size, gen_len)

    def evaluate(self, T=100, p_mut=.5, p_gene_mut=.5):
        t = 0
        init_population = [[randint(0, 1) for y in range(self._get_gen_length())]
                           for x in range(self._get_pop_size())]

        weighted_pop = [[x, self._get_fitness()(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)
        while t < T:
            print(t)
            if self._get_fittest() is None and self._get_max_fitness() is None:
                self._set_fittest(weighted_pop[0][0])
                self._set_max_fitness(weighted_pop[0][1])

            elif weighted_pop[0][1] > self._get_max_fitness():
                self._set_fittest(weighted_pop[0][0])
                self._set_max_fitness(weighted_pop[0][1])

            self._add_to_memory([self._get_max_fitness(), t])
            parents = self._get_kernel().parent_selection(weighted_pop)
            parents = sample(parents, 2)
            _, newborns = self._get_kernel().recombination(parents[0][0], parents[1][0])
            for individual in range(len(newborns)):
                newborns[individual] = self._get_kernel().mutation(newborns[individual], p_mut=p_gene_mut) \
                    if random() <= p_mut else newborns[individual]
            weighted_pop[parents[0][1]], weighted_pop[parents[1][1]] = [newborns[0],
                                                                        self._get_fitness()(newborns[0])], \
                                                                       [newborns[1],
                                                                        self._get_fitness()(newborns[1])]
            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            t += 1
        if self._get_fittest() is None and self._get_max_fitness() is None:
            self._set_fittest(weighted_pop[0][0])
            self._set_max_fitness(weighted_pop[0][1])

        elif weighted_pop[0][1] > self._get_max_fitness():
            self._set_fittest(weighted_pop[0][0])
            self._set_max_fitness(weighted_pop[0][1])

        self._add_to_memory([self._get_max_fitness(), t])
        return self._get_fittest()
