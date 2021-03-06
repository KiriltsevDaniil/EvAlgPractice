from random import randint, random


def point_mutation(individual, p_mut=0.5, points=1):
    for i in range(points):
        chosen = randint(0, len(individual)-1)
        if random() <= p_mut: individual[chosen] = individual[chosen] ^ 1
    return individual


def group_mutation(individual, p_mut=0.5):
    chain_iterator = randint(0, len(individual) - 1)
    chain_length = randint(2, len(individual) - 1)
    if random() <= p_mut:
        while chain_iterator <= len(individual) - 1 and chain_length != 0:
            individual[chain_iterator] = individual[chain_iterator] ^ 1
            chain_iterator, chain_length = chain_iterator + 1, chain_length - 1
    return individual


def density_mutation(individual, p_mut=0.2):
    for i in range(len(individual)):
        if random() <= p_mut:
            individual[i] = individual[i] ^ 1
    return individual


def exchange_mutation(individual, p_mut=0.5):
    if random() <= p_mut:
        if len(individual) == 3:
            individual[1], individual[2] = individual[2], individual[1]
        elif len(individual) == 2:
            return individual
        else:
            pivot = randint(2, len(individual) - 2) # changed for stock problem
            individual[pivot - 1], individual[pivot + 1] = individual[pivot + 1], individual[pivot - 1]
    return individual
    