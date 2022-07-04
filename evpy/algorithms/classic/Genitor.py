from genetic_operators.OperatorKernel import KernelBox
from random import randint, random

class Genitor:
    '''Genitor GA (Whitley's model)'''
    def __init__(self, fitness, recombination, mutator, pop_size=5, g_len=10):
        self.pop_size = pop_size
        self.g_len = g_len
        self.kernel = KernelBox(algorithm="Genitor", recombination=recombination, mutator=mutator)
        self.get_fitness = fitness
        self.memory = []
        self.fittest = None
        self.max_fitness = None

    def evaluate(self, T=100, p_gene_mut=.5, p_mut=.5):
        t,  equilibrium = 0, False
        init_population = [[randint(0,1) for y in range(self.g_len)] for x in range(self.pop_size)]
        weighted_pop = [[x, self.get_fitness(x)] for x in init_population]
        weighted_pop.sort(key=lambda x: x[1], reverse=True)
        for i in range(1, len(weighted_pop)):
            if weighted_pop[i][1] != weighted_pop[i-1][1]:
                break
            if i == (len(weighted_pop) - 1) and weighted_pop[i][1] == weighted_pop[i-1][1]:
                equilibrium = True
        while not equilibrium and t < T:
            print(t)
            if self.fittest == None and self.max_fitness == None:
                self.fittest, self.max_fitness = weighted_pop[0]
            elif weighted_pop[0][1] > self.max_fitness:
                self.fittest, self.max_fitness = weighted_pop[0]
            self.memory.append([self.max_fitness, t])

            parents = self.kernel.parent_selection(weighted_pop)
            _, children = self.kernel.recombination(parents[0], parents[1])
            child = children[randint(0, 1)]
            child = self.kernel.mutation(child, p_mut=p_gene_mut) if random() <= p_mut else child
            child = [child, self.get_fitness(child)]
            weighted_pop[-1] = child

            weighted_pop.sort(key=lambda x: x[1], reverse=True)
            for i in range(1, len(weighted_pop)):
                if weighted_pop[i][1] != weighted_pop[i-1][1]:
                    break
                if i == (len(weighted_pop) - 1) and weighted_pop[i][1] == weighted_pop[i-1][1]:
                    equilibrium = True
            t += 1

        if self.fittest == None and self.max_fitness == None:
            self.fittest, self.max_fitness = weighted_pop[0]
        elif weighted_pop[0][1] > self.max_fitness:
            self.fittest, self.max_fitness = weighted_pop[0]
        self.memory.append([self.max_fitness, t])
        return self.fittest