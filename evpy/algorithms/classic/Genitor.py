from evpy.wrappers.facade.kernel import Kernel
from evpy.algorithms.base.algorithm import Algorithm

from random import randint, random


def make_genitor(kernel: Kernel, fitness: callable, pop_size: int, gen_len: int):
    return Genitor(kernel, fitness, pop_size, gen_len)


class Genitor(Algorithm):
    '''
    Genitor GA (Whitley's model)

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
    def __init__(self, kernel: Kernel, fitness: callable, pop_size: int=5, gen_len: int=10):
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

    def check_equilibrium(self, weighted_pop: list) -> bool:
        '''
        This function checks convergence of the algorithm.

        Parameters
        ----------
        weighted_pop : list
            This parameter contains evaluated current population.
        
        Returns
        -------
        bool
            returns True if the algorithm converged, otherwise False
        '''
        equilibrium = False
        for i in range(1, len(weighted_pop)):
                if weighted_pop[i][1] != weighted_pop[i-1][1]: break
                if i == (len(weighted_pop) - 1) and weighted_pop[i][1] == weighted_pop[i-1][1]: equilibrium = True

        return equilibrium

    def evaluate(self, T: int=100, p_gene_mut: float=.5, p_mut: float=.5) -> list:
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
            returns the fittest individual among all generations
        '''
        t,  equilibrium = 0, False
        init_population = [[randint(0, 1) for y in range(self._get_gen_length())] for x in range(self._get_pop_size())]
        weighted_pop = [[x, self._get_fitness()(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)

        equilibrium = self.check_equilibrium(weighted_pop)
        while not equilibrium and t < T:
            print(f"Generation: {t}/{T}") if t % (T//10) == 0 else None
            self.memory_update(weighted_pop, t)

            # Choosing parents
            parents = self._get_kernel().parent_selection(weighted_pop)

            # Recombination
            _, children = self._get_kernel().recombination(parents[0], parents[1])
            child = children[randint(0, 1)]

            # Mutation
            child = self._get_kernel().mutation(child, p_mut=p_gene_mut) if random() <= p_mut else child
            
            # New population formation
            weighted_pop[-1] = [child, self._get_fitness()(child)]
            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            equilibrium = self.check_equilibrium(weighted_pop)
            t += 1
        self.memory_update(weighted_pop, t)

        return self._get_fittest()
