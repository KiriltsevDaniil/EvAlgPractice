from evpy.algorithms.base.parallel import make_parallel


class ParallelFactory:
    def __init__(self, parallel_builder: callable = None):

        if parallel_builder is None:
            parallel_builder = make_parallel

        self.builder = parallel_builder

    def _make_parallel(self, archipelago: list, fitness_function: callable, rule: callable = None):
        return self.builder(archipelago, fitness_function, rule)
    