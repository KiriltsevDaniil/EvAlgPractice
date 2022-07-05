# command module to wrap genetic operators


class Command(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args):

        if 2 <= len(args) < 3:
            par_1, par_2 = args[0], args[1]
            return self.function(par_1, par_2)

        elif 3 <= len(args) < 4:
            par_1, par_2, par_3 = args[0], args[1], args[2]
            return self.function(par_1, par_2, par_3)

        else:
            par_1, par_2, par_3, par_4 = args[0], args[1], args[2], args[3]
            return self.function(par_1, par_2, par_3, par_4)
