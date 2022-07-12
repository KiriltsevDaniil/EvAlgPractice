from Task.Logger.observer import Observer


class Publisher(object):
    def __init__(self):
        self.__observers = []

    def subscribe(self, observer: Observer):
        self.__observers.append(observer)

    def notify(self, message, no_time=False):
        for obs in self.__observers:
            obs.update(message, no_time)
