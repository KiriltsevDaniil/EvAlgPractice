from evpy.genetic_operators.recombination.crossover import single_point_crossover, double_point_crossover, \
    multi_point_crossover, shuffler_crossover, single_point_rsc
from evpy.genetic_operators.recombination.rvrecombination import intermediate_recombination, \
    linear_recombination
from evpy.genetic_operators.recombination.discrete import discrete_recombination
from evpy.genetic_operators.mutators.bimutators import point_mutation, group_mutation, density_mutation, \
    exchange_mutation
from evpy.genetic_operators.mutators.rvmutators import real_valued_mutation
from evpy.genetic_operators.selectors.population_selection import truncation_selection, elite_selection, \
    bolzman_selection
from evpy.genetic_operators.selectors.parent_selection import random_couple, panmixia, outbreeding, \
    inbreeding, tournament_selection, fitness_proportional_selection

from random import sample


#   A collection of all supported commands
class CommandList:
    def __init__(self, commands=None):

        supported = {
            "mutation": {"point_mutation": point_mutation,
                         "group_mutation": group_mutation,
                         "density_mutation": density_mutation,
                         "exchange_mutation": exchange_mutation,
                         "real_valued_mutation": real_valued_mutation},

            "recombination": {"single_point_crossover": single_point_crossover,
                              "double_point_crossover": double_point_crossover,
                              "multi_point_crossover": multi_point_crossover,
                              "shuffler_crossover": shuffler_crossover,
                              "single_point_rsc": single_point_rsc,

                              "intermediate_recombination": intermediate_recombination,
                              "linear_recombination": linear_recombination,

                              "discrete": discrete_recombination
                              },

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

        if commands is None:
            self.__commands = supported
        else:
            self.__commands = commands

    def show_supported(self):
        return list(self.__commands.keys())

    def add_category(self, category: str, addition=None):

        if not addition:
            addition = dict()

        if category not in self.__commands:
            self.__commands[category] = addition

    def add_command(self, category: str, name: str, command, replace=False):

        if category in self.__commands:

            if (name in self.__commands[category] and replace) or name not in self.__commands[category]:
                self.__commands[category][name] = command

        else:
            self.__commands[category] = dict()
            self.__commands[category][name] = command

    def get_command(self, name: str):

        for category in self.__commands:
            if name in self.__commands[category]:
                return self.__commands[category][name]

        raise KeyError("No such operator found!")

    def get_random(self, category: str):
        if category in self.__commands:
            return sample(list(self.__commands[category].values()), k=1)[0]

    def check_category(self, category: str):
        if category in self.__commands:
            return True
        return False

    def check_function(self, name: str):
        for category in self.__commands:
            if name in self.__commands[category]:
                return True

        return False
