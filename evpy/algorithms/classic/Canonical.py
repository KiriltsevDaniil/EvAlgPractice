from evpy.algorithms.base.algorithm import Algorithm
from evpy.wrappers.facade.kernel import Kernel

from time import perf_counter
from random import randint, sample, random


def make_canonical(kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
    return Canonical(kernel, fitness, pop_size, gen_len)


class Canonical(Algorithm):
    '''
    Canonical GA (Holland's model)
    
    Attributes
    ----------
    __get_fitness: function
        This attribute contains fitness function.
    __kernel: Kernel
        This attribute contains kernel.
    __memory : list
        This attribute contains the maximum fitness of each previous generation.
    __current_population : list
        this attribute contains population of the current generation.
    __fittest : list
        This attribute contains the fittes individual among all previous generations.
    __max_fitness : float
         This attribute contains the maximum fitness among all previous generations.
    __pop_size : int
        This attribute contains size of the population.
    __gen_length : int
        This attribute contains word length of genes.
    '''

    def __init__(self, kernel: Kernel, fitness: callable, pop_size: int = 5, gen_len: int = 10):
        '''
        Parameters
        ----------
        kernel : Kernel
            The main purpose of the kernel is to provide certain genetic operators to GA.
        fitness : function
            Fitness is used to evaluate the quality of an individual.
        pop_size : int, optional
            Pop_size parameter responsible for population size.
        gen_len : int, optional
            Gen_len parameter responsible for word length of genes.
        '''
        super().__init__(kernel, fitness, pop_size, gen_len)

    def memory_update(self, weighted_pop: list, t: int) -> None:
        '''
        This function updates algorithm's memory list.

        Parameters
        ----------
        weighted_pop : list
            This parameter contains evaluated current population 
        t : int
            This parameter contains number of generation.
        '''
        fittest, fitness = weighted_pop[0]
        if self._get_fittest() is None and self._get_max_fitness() is None:
            self._set_fittest(fittest)
            self._set_max_fitness(fitness)
        elif fitness > self._get_max_fitness():
            self._set_fittest(fittest)
            self._set_max_fitness(fitness)
        self._set_current([x[0] for x in weighted_pop])
        self._add_to_memory([self._get_max_fitness(), t])

        return

    def evaluate(self, T: int = 2000, p_gene_mut: float = .5, p_mut: float = .5) -> list:
        '''
        Parameters
        ----------
        T : int
            The number of generations after which the algorithm ends.
        p_mut : float
            The probability of mutation of the offspring after birth.
        p_gene_mut : float
            The probability of gene mutation.
        
        Returns
        -------
        list
            returns the fittest individual among all generations.
        '''
        starting_point = perf_counter()
        t = 0
        if self._get_current() is None:
            init_population = [[randint(0, 1) for y in range(self._get_gen_length())] for x in
                               range(self._get_pop_size())]
        else:
            init_population = self._get_current()
        weighted_pop = [[x, self._get_fitness()(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)
        while t < T:
            print(f"Generation: {t}/{T}") if t % (T // 10) == 0 else None
            self.memory_update(weighted_pop, t)

            # Choosing parents
            parents = sample(self._get_kernel().parent_selection(weighted_pop), 2)

            # Recombination
            _, newborns = self._get_kernel().recombination(parents[0][0], parents[1][0])

            # Mutation
            for individual in range(len(newborns)):
                newborns[individual] = self._get_kernel().mutation(newborns[individual], p_mut=p_gene_mut) \
                    if random() <= p_mut else newborns[individual]

            # New population formation
            weighted_pop[parents[0][1]], weighted_pop[parents[1][1]] = [newborns[0],
                                                                        self._get_fitness()(newborns[0])], \
                                                                       [newborns[1],
                                                                        self._get_fitness()(newborns[1])]
            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            t += 1
        self.memory_update(weighted_pop, t)
        ending_point = perf_counter()
        self._set_convergence_time(round(ending_point - starting_point, 2))
        print(f"Model took {self._get_convergence_time()} second(s) to converge. [Canonical Model]")
        return self._get_fittest()
