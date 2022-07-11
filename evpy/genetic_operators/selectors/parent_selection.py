from random import randint, sample, random


# Structure: we take dirty/clean population, we return lists of pairs of parents
def random_couple(weighted_population):
    weighted_population = [[weighted_population[x][0], weighted_population[x][1], x]
                           for x in range(len(weighted_population))]
    parents = sample(weighted_population, k=2)
    return [x[2] for x in parents]


def panmixia(weighted_population):
    parents = [[x[0], weighted_population[randint(len(weighted_population) - 1)]][0]
        for x in weighted_population]
    parents = list(filter(lambda x: x[0] != x[1], parents))
    return parents


def outbreeding(weighted_population, metric, ammount=1):
    population = [x[0] for x in weighted_population]
    chosens = [randint(0, len(population) - 1) for x in range(ammount)]
    parents = []
    maximum = None
    
    for chosen in chosens:
        for i in range(population):
            if chosen != i:
                score = metric(population[chosen], population[i])
                maximum = [i , score] if maximum == None else [i , score] if score > maximum else maximum   
        parents.append([population[chosen], population[maximum[0]]])
    return parents


def inbreeding(weighted_population, metric, ammount=1):
    population = [x[0] for x in weighted_population]
    chosens = [randint(0, len(population) - 1) for x in range(ammount)]
    parents = []
    minimum = None
    
    for chosen in chosens:
        for i in range(population):
            if chosen != i:
                score = metric(population[chosen], population[i])
                minimum = [i , score] if minimum == None else [i , score] if score < minimum else minimum   
        parents.append([population[chosen], population[minimum[0]]])
    return parents


def tournament_selection(weighted_population, tournament_k=2):
    winners = []
    ordered_population = [[weighted_population[i][0], weighted_population[i][1], i] for i 
    in range(len(weighted_population))]
    
    for i in range(ordered_population):
        competitors = sample(ordered_population, k=tournament_k)
        competitors.sort(key=lambda x: x[1], reverse=True)
        winners.append[competitors[0][0], competitors[0][1]]
        ordered_population = list(filter(lambda x: x[2] != competitors[0][2], ordered_population))
    
    return panmixia(winners)


def fitness_proportional_selection(weighted_population):
    ordered_population = [x + [i] for i, x in enumerate(weighted_population)]
    cumulative_fitness = sum([x[1] for x in ordered_population])
    probs = [x[1]/cumulative_fitness for x in ordered_population]
    cdf = [sum(probs[:i+1]) for i in range(len(probs))]
    parents = []
    for n in range(len(ordered_population)):
        point = random()
        for i in range(len(ordered_population)):
            if point <= cdf[i]:
                parents.append([ordered_population[i][0], ordered_population[i][2]])
                break
    return parents
