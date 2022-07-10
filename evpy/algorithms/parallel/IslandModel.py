from evpy.algorithms.base.parallel import Parallel
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


def make_island_model(archipelago: list, fitness_function: callable, rule: callable = None):
    return IslandModel(archipelago, fitness_function, rule)


class IslandModel(Parallel):
    def __init__(self, archipelago: list, fitness_function: callable, rule: callable = None):

        if rule is None:
            rule = self.clockwise

        super().__init__(archipelago, fitness_function, rule)

    def clockwise(self, results):
        for i in range(1, len(results) - 1):
            current_pop = self._get_archipelago()[i]._get_current()
            current_pop[-1] = results[i - 1]
            self._get_archipelago()[i]._set_current(current_pop)
        current_pop = self._get_archipelago()[0]._get_current()
        current_pop[-1] = results[-1]
        self._get_archipelago()[0]._set_current(current_pop)

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
        self._add_to_memory([self._get_max_fitness(), t])

        return

    def evaluate(self, M: int, *args) -> list:
        executor = ThreadPoolExecutor()
        starting_point = perf_counter()
        for m in range(M):
            print(f"Generation: {m}/{M}") if m % (M // 10) == 0 else None
            threads = [executor.submit(self._get_archipelago()[i].evaluate, *args[i]) for i in
                       range(len(self._get_archipelago()))]
            results = []
            for task in threads:
                results.append(task.result())

            if m != M - 1: self._migrate()(results)
            self.memory_update([[x, self._get_fitness()(x)] for x in results], m)
        ending_point = perf_counter()
        self._set_convergence_time(round(ending_point - starting_point, 2))
        print(f"Model took {self._get_convergence_time()} second(s) to converge. [Island Model]")

        return self._get_fittest()
