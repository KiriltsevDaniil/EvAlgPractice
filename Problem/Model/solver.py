from evpy.algorithms.base.classic import Classic
from evpy.wrappers.facade.kernel import Kernel

from Problem.Model.solution import Solution

from time import perf_counter
from random import sample, random


class Solver(Classic):
    def __init__(self, kernel: Kernel, fitness: callable, rectangles: list, pop_size: int, gen_len: int):
        super().__init__(kernel, fitness, pop_size, gen_len)

        rectangles.sort(key=lambda x: x.get_height() * x.get_width(), reverse=True)

        self.solution = Solution(rectangles)

    def evaluate(self, T: int =100, p_mut: float =.5, p_gene_mut: float =.5):
        starting_point = perf_counter()
        t = 0
        if self._get_current() is None:
            # init_population = [sample([x for x in range(1, self._get_pop_size() + 1)], k=self._get_gen_length())
            #                    for x in range(1, self._get_pop_size() + 2)]

            init_population = [[1] + sample([x for x in range(2, self._get_pop_size() + 1)],
                                k=self._get_gen_length() - 1) for x in range(self._get_pop_size())]
        else:
            init_population = self._get_current()

        weighted_pop = [[x, self._get_fitness()(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1])
        while t < T:
            # print(f"Generation: {t}/{T}") if t % (T // 10) == 0 else None
            self.memory_update(weighted_pop, t)

            # Choosing parents
            parents = sample(self._get_kernel().parent_selection(weighted_pop), k=2)
            parents = [[weighted_pop[parents[0]][0], parents[0]], [weighted_pop[parents[1]][0], parents[1]]]
            self.solution.set_parents([parents[0][0], parents[1][0]])
            parents = [[parents[0][0], parents[0][1], self._get_fitness()(parents[0][0])],
                       [parents[1][0], parents[1][1], self._get_fitness()(parents[1][0])]]

            print(f"parents: {parents}")

            # Recombination
            _, newborns = self._get_kernel().recombination(parents[0][0], parents[1][0])
            print(f"kinder: {newborns}")

            # Mutation
            for individual in range(len(newborns)):
                newborns[individual] = self._get_kernel().mutation(newborns[individual], p_mut=p_gene_mut) \
                    if random() <= p_mut else newborns[individual]

            # New population formation
            weighted_pop[parents[0][1]], weighted_pop[parents[1][1]] = [newborns[0],
                                                                        self._get_fitness()(newborns[0])], \
                                                                       [newborns[1],
                                                                        self._get_fitness()(newborns[1])]

            weighted_pop.sort(key=lambda x: x[1])
            population = [x[0] for x in weighted_pop]
            self.solution.set_population(population)
            self.solution.set_fittest(population[0])
            self.solution.set_fitness(self._get_fitness()(self.solution.get_fittest()))

            t += 1

        self.memory_update(weighted_pop, t)
        ending_point = perf_counter()
        self._set_convergence_time(round(ending_point - starting_point, 2))
        print(f"Model took {self._get_convergence_time()} second(s) to converge. [Canonical Model]")

        return self.solution

    def memory_update(self, weighted_pop: list, t: int) -> None:
        fittest, fitness = weighted_pop[0]
        if self._get_fittest() is None and self._get_max_fitness() is None:
            self._set_fittest(fittest)
            self._set_max_fitness(fitness)
        elif fitness > self._get_max_fitness():
            self._set_fittest(fittest)
            self._set_max_fitness(fitness)
        self._set_current([x[0] for x in weighted_pop])
        self._add_to_memory([self._get_max_fitness(), t])
