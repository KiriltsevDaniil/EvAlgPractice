import genetic_operators.mutators.bimutators as bimutators
import genetic_operators.recombination.crossover as crossover
import genetic_operators.mutators.rvmutators as rvmutators
import genetic_operators.recombination.rvrecombination as rvrecombination
import genetic_operators.recombination.discrete as discrete
import genetic_operators.selectors.parent_selection as parent_selection

crossover_opts = {
    "single_point_crossover": crossover.single_point_crossover,
    "double_point_crossover": crossover.double_point_crossover, 
    "multi_point_crossover": crossover.multi_point_crossover,
    "shuffler_crossover": crossover.shuffler_crossover, 
    "single_point_rsc": crossover.single_point_crossover
}
discrete_opts = {
    "discrete": discrete.discrete_recombination
}
rvrecombination_opts = {
    "intermediate_recombination": rvrecombination.intermediate_recombination,
    "linear_recombination": rvrecombination.linear_recombination
}
bimutator_opts = {
    "point_mutation": bimutators.point_mutation,
    "group_mutation": bimutators.group_mutation,
    "density_mutation": bimutators.density_mutation,
    "exchange_mutation": bimutators.exchange_mutation
}
rvmutator_opts = {
    "real_valued_mutation": rvmutators.real_valued_mutation
}



class KernelBox:
    def __init__(self, algorithm, **kwargs):
        if algorithm == 'Canonical':
            self.selection = None
            self.parent_selection = parent_selection.fitness_proportional_selection
            self.recombination = crossover.single_point_crossover
            self.mutation = bimutators.point_mutation
        
        elif algorithm == 'Genitor':
            self.selection = None
            self.parent_selection = parent_selection.random_couple
            
            for operator, opt in kwargs.items():
                if opt in crossover_opts:
                    self.recombination = crossover_opts[opt]
                elif opt in discrete_opts:
                    self.recombination = discrete_opts[opt]
                elif opt in rvrecombination_opts:
                    self.recombination = rvrecombination_opts[opt]
                elif opt in bimutator_opts:
                        self.mutation = bimutator_opts[opt]
                elif opt in rvmutator_opts:
                        self.mutation = rvmutator_opts[opt]


class Kernel:
    def __init__(self):
        pass