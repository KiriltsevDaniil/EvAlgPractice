from genetic_operators.OperatorKernel import KernelBox
from random import randint, sample, random

class Canonical:
    '''Canonical GA (Holland's model)'''
    def __init__(self, fitness, pop_size=5, g_len=10):
        self.pop_size = pop_size
        self.g_len = g_len
        self.kernel = KernelBox(algorithm="Canonical")
        self.get_fitness = fitness
        self.memory = []
        self.fittest = None
        self.max_fitness = None

    def evaluate(self, T=100, p_mut=.5, p_gene_mut=.5):
        t = 0
        init_population = [[randint(0,1) for y in range(self.g_len)] for x in range(self.pop_size)]
        weighted_pop = [[x, self.get_fitness(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)
        while t < T:
            print(t)
            if self.fittest == None and self.max_fitness == None:
                self.fittest, self.max_fitness = weighted_pop[0]
            elif weighted_pop[0][1] > self.max_fitness:
                self.fittest, self.max_fitness = weighted_pop[0]
            self.memory.append([self.max_fitness, t])
            parents = self.kernel.parent_selection(weighted_pop)
            parents = sample(parents, 2)
            _, newborns = self.kernel.recombination(parents[0][0], parents[1][0])
            for individual in range(len(newborns)):
                newborns[individual] = self.kernel.mutation(newborns[individual], p_mut=p_gene_mut) if random() <= p_mut else newborns[individual]
            weighted_pop[parents[0][1]], weighted_pop[parents[1][1]] = [newborns[0], self.get_fitness(newborns[0])], [newborns[1], self.get_fitness(newborns[1])]
            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            t += 1
        if self.fittest == None and self.max_fitness == None:
                self.fittest, self.max_fitness = weighted_pop[0]
        elif weighted_pop[0][1] > self.max_fitness:
            self.fittest, self.max_fitness = weighted_pop[0]
        self.memory.append([self.max_fitness, t])
        return self.fittest