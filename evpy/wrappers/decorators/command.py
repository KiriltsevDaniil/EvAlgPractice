# factory method for Command
def make_command(function):
    return Command(function)


# command module to wrap genetic operators
class Command(object):
    def __init__(self, function: callable):
        self.__function = function

    def __call__(self, *args, **kwargs):
        return self.__function(*args, **kwargs)

