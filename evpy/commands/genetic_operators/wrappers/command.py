# factory method for Command
def make_com(function):
    return Command(function)


# command module to wrap genetic operators
class Command(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, **kwargs):
        # (!) as of now parsing as positional arguments, need to figure out how to parse as named in case of abstract
        # function

        if len(kwargs.keys()) == 1:
            par_1 = list(kwargs.values())[0]
            return self.function(par_1)

        elif 2 <= len(kwargs) < 3:
            parameters = list(kwargs.values())
            par_1, par_2 = parameters[0], parameters[1]
            return self.function(par_1, par_2)

        elif 3 <= len(kwargs) < 4:
            parameters = list(kwargs.values())
            par_1, par_2, par_3 = parameters[0], parameters[1], parameters[2]
            return self.function(par_1, par_2, par_3)

        else:
            parameters = list(kwargs.values())
            par_1, par_2, par_3, par_4 = parameters[0], parameters[1], parameters[2], parameters[3]
            return self.function(par_1, par_2, par_3, par_4)
