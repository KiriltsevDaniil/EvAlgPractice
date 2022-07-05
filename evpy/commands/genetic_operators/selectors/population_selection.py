from audioop import reverse
from math import exp
from random import random, sample

def truncation_selection(weighted_population, newpop_size):
    weighted_population.sort(key=lambda x: x[1], reverse=True)
    new_population = [x[0] for x in weighted_population[:newpop_size-1]]
    return new_population

def elite_selection(weighted_population, auxiliary_selection, elite_size, newpop_size):
    weighted_population.sort(key=lambda x: x[1], reverse=True)
    new_population = [x[0] for x in weighted_population[:elite_size-1]]
    new_population += auxiliary_selection(weighted_population[:elite_size-1], newpop_size - elite_size)
    return new_population

def bolzman_selection(weighted_population, newpop_size, temperature=2):
    new_population = []
    while len(new_population < newpop_size):
        candidates = sample(range(len(weighted_population)), k=2)
        p = 1/(1 + exp((weighted_population[candidates[0]][1]- weighted_population[candidates[1]][1])/temperature))
        new_population.append(weighted_population.pop(candidates[0])[0]) if random() <= p else new_population.append(
        weighted_population.pop(candidates[1])[0])
    return new_population
    