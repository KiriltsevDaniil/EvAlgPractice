from evpy.algorithms.base.classic import Classic
from evpy.wrappers.facade.kernel import Kernel

from Problem.genetic_algorithm.solution import Solution
from Problem.genetic_algorithm.population import Population

from time import perf_counter
from random import sample, random


class Solver(Classic):
    def __init__(self, kernel: Kernel, fitness: callable, rectangles: list, pop_size: int, gen_len: int):
        super(Solver, self).__init__(kernel, fitness, pop_size, gen_len)

        rectangles.sort(key=lambda x: x.get_height() * x.get_width(), reverse=True)
        self.rectangles = rectangles

    def evaluate(self, T: int =100, p_mut: float =.5, p_gene_mut: float =.5):
        flag = False
        self.notify("algorithm started")

        starting_point = perf_counter()
        t = 0

        if self._get_current() is None:

            init_population = [[1] + sample([x for x in range(2, self._get_pop_size() + 1)],
                                k=self._get_gen_length() - 1) for x in range(self._get_pop_size())]

            self.notify(f"starting population: {init_population}")

            weighted_population = []
            for index, genotype in enumerate(init_population):
                individual = Solution(self.rectangles, genotype, index)
                individual.set_fitness(self._get_fitness()(individual))

                weighted_population.append(individual)
        else:
            weighted_population = self._get_current()
            flag = True

        weighted_population.sort(key=lambda x: x.get_fitness())

        self.notify("-" * 75, True)

        while t < T:

            self.notify(f"step {t + 1}:\n")
            
            if not flag:
                self.memory_update(weighted_population, t)
            if T > 1:
                flag = False
            # Choosing parents
            parents = sample(self._get_kernel().parent_selection(weighted_population), k=2)
            self.notify(f"parents: [{parents[0].get_genotype()}, {parents[1].get_genotype()}]")

            # Recombination
            _, newborns = self._get_kernel().recombination(parents[0].get_genotype(), parents[1].get_genotype())
            self.notify(f"offsprings: [{newborns[0]}, {newborns[1]}]")

            before_mutation = f"[{newborns[0]}, {newborns[1]}]"

            # Mutation
            for individual in range(len(newborns)):
                newborns[individual] = self._get_kernel().mutation(newborns[individual], p_mut=p_gene_mut) \
                    if random() <= p_mut else newborns[individual]

            self.notify(f"mutation:" + before_mutation + f" => [{newborns[0]}, {newborns[1]}]")

            # New population formation
            newborn_1 = Solution(self.rectangles, newborns[0], parents[0].get_id())
            newborn_1.set_fitness(self._get_fitness()(newborn_1))
            newborn_1.set_parents([x.get_genotype() for x in parents])

            newborn_2 = Solution(self.rectangles, newborns[1], parents[1].get_id())
            newborn_2.set_fitness(self._get_fitness()(newborn_2))
            newborn_2.set_parents([x.get_genotype() for x in parents])

            weighted_population[weighted_population.index(parents[0])] = newborn_1
            weighted_population[weighted_population.index(parents[1])] = newborn_2

            weighted_population.sort(key=lambda x: x.get_fitness())

            t += 1

            self.notify("-" * 75, True)

        self.memory_update(weighted_population, t)
        ending_point = perf_counter()
        self._set_convergence_time(round(ending_point - starting_point, 2))
        self.notify(f"Model took {self._get_convergence_time()} second(s) to converge. [Canonical Model]")

        return self._get_memory()

    def memory_update(self, weighted_pop, t: int) -> None:
        fittest, fitness = weighted_pop[0].get_genotype(), weighted_pop[0].get_fitness()

        if self._get_fittest() is None and self._get_max_fitness() is None:
            self._set_fittest(fittest)
            self._set_max_fitness(fitness)

        elif fitness > self._get_max_fitness():

            self._set_fittest(fittest)
            self._set_max_fitness(fitness)

        self._set_current(weighted_pop)
        self._add_to_memory(Population(weighted_pop, t))
