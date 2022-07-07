# factory method for Command
def make_command(function):
    return Command(function)


# command module to wrap genetic operators
class Command(object):
    def __init__(self, function):
        self.__function = function

    def __call__(self, *args, **kwargs):
        # (!) as of now parsing as positional arguments, need to figure out how to parse as named in case of abstract
        # function

        if len(args) < 1:

            if len(kwargs.keys()) < 1:
                return -1

            elif len(kwargs.keys()) == 1:
                par_1 = list(kwargs.values())[0]
                return self.__function(par_1)

            elif 2 <= len(kwargs) < 3:
                parameters = list(kwargs.values())
                par_1, par_2 = parameters[0], parameters[1]
                return self.__function(par_1, par_2)

            elif 3 <= len(kwargs) < 4:
                parameters = list(kwargs.values())
                par_1, par_2, par_3 = parameters[0], parameters[1], parameters[2]
                return self.__function(par_1, par_2, par_3)

            else:
                parameters = list(kwargs.values())
                par_1, par_2, par_3, par_4 = parameters[0], parameters[1], parameters[2], parameters[3]
                return self.__function(par_1, par_2, par_3, par_4)

        else:
            if len(args) == 1:
                return self.__function(args[0])

            elif 2 <= len(args) < 3:
                return self.__function(args[0], args[1])

            elif 3 <= len(kwargs) < 4:
                return self.__function(args[0], args[1], args[2])

            else:
                return self.__function(args[0], args[1], args[2], args[3])