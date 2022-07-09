from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


class IslandModel:
    def __init__(self, archipelago: list, fitness_function: callable, rule: callable=None) -> list:
        self.__archipelago = archipelago
        self.__migrate = rule
        self.__fitness = fitness_function
        self.__fittest = None
        self.__max_fitness = None
        self.__memory = []
        if rule == None: self.__migrate = self.clockwise
        self.__convergence_time = None

    def _get_convergence_time(self):
        return self.__convergence_time

    def _set_convergence_time(self, time):
        self.__convergence_time = time

    def _get_memory(self):
        return self.__memory

    def _get_max_fitness(self):
        return self.__max_fitness

    def clockwise(self, results):
        for i in range(1, len(results) - 1):
            current_pop = self.__archipelago[i]._get_current()
            current_pop[-1] = results[i-1]
            self.__archipelago[i]._set_current(current_pop)
        current_pop = self.__archipelago[0]._get_current()
        current_pop[-1] = results[-1]
        self.__archipelago[0]._set_current(current_pop)

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
        if self.__fittest is None and self.__max_fitness is None:
            self.__fittest = fittest
            self.__max_fitness = fitness
        elif fitness > self._get_max_fitness():
            self.__fittest = fittest
            self.__max_fitness = fitness
        self.__memory.append([self._get_max_fitness(), t])
        
        return

    def evaluate(self,  M: int, *args) -> list:
        executor = ThreadPoolExecutor()
        starting_point = perf_counter()
        for m in range(M):
            print(f"Generation: {m}/{M}") if m % (M//10) == 0 else None
            threads = [executor.submit(self.__archipelago[i].evaluate, *args[i]) for i in range(len(self.__archipelago))]
            results = []
            for task in threads:
                results.append(task.result())
            
            
            if m != M - 1: self.__migrate(results)
            self.memory_update([[x, self.__fitness(x)] for x in results],m)
        ending_point = perf_counter()
        self._set_convergence_time(round(ending_point - starting_point, 2))
        print(f"Model took {self._get_convergence_time()} second(s) to converge. [Island Model]")
        return self.__fittest