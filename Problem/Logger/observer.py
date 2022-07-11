from datetime import datetime


class Observer:
    def __init__(self):
        self.__event_log = []

    def update(self, message, no_time=False):
        current_time = datetime.now()
        time_string = current_time.strftime("%H:%M:%S")

        if no_time:
            self.__event_log.append(f"{message}")
        else:
            self.__event_log.append(f"[{time_string}] {message}")

    def get_logs(self):
        return self.__event_log

    def clear_logs(self):
        del self.__event_log
        self.__event_log = []
