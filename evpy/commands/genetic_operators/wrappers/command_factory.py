from random import sample

from evpy.commands.genetic_operators.wrappers.command import make_com
from evpy.commands.genetic_operators.recombination.crossover import single_point_crossover, double_point_crossover, \
    multi_point_crossover, shuffler_crossover, single_point_rsc
from evpy.commands.genetic_operators.recombination.rvrecombination import intermediate_recombination, \
    linear_recombination
from evpy.commands.genetic_operators.recombination.discrete import discrete_recombination
from evpy.commands.genetic_operators.mutators.bimutators import point_mutation, group_mutation, density_mutation, \
    exchange_mutation
from evpy.commands.genetic_operators.mutators.rvmutators import real_valued_mutation
from evpy.commands.genetic_operators.selectors.population_selection import truncation_selection, elite_selection, \
    bolzman_selection
from evpy.commands.genetic_operators.selectors.parent_selection import random_couple, panmixia, outbreeding, \
    inbreeding, tournament_selection, fitness_proportional_selection

class CommandFactory:
    def __init__(self, factory_func=make_com):

        self.factory = factory_func

        self.products = {
            "recombination": {"single_point_crossover": single_point_crossover,
                              "double_point_crossover": double_point_crossover,
                              "multi_point_crossover": multi_point_crossover,
                              "shuffler_crossover": shuffler_crossover,
                              "single_point_rsc": single_point_rsc,

                              "intermediate_recombination": intermediate_recombination,
                              "linear_recombination": linear_recombination,

                              "discrete": discrete_recombination
                              },

            "mutation": {"point_mutation": point_mutation,
                         "group_mutation": group_mutation,
                         "density_mutation": density_mutation,
                         "exchange_mutation": exchange_mutation,
                         "real_valued_mutation": real_valued_mutation},

            "population_selector": {
                "truncation_selection": truncation_selection,
                "elite_selection": elite_selection,
                "bolzman_selection": bolzman_selection
            },

            "parent_selector": {
                "random_couple": random_couple,
                "panmixia": panmixia,
                "outbreeding": outbreeding,
                "inbreeding": inbreeding,
                "tournament_selection": tournament_selection,
                "fitness_proportional_selection": fitness_proportional_selection
            }
        }

    def add_product(self, category: str, products: dict):
        self.products[category] = products

    def get_categories(self):
        return self.products.keys()

    def make_command(self, tag: str, func=""):
        if tag in self.products:
            if func in self.products[tag]:
                return self.factory(self.products[tag][func])
            else:
                return self.factory(sample(list(self.products[tag].values()), k=1))


factorio = CommandFactory()
com1 = factorio.make_command("mutation")
print(com1(dict()))
