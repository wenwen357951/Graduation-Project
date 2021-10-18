import time


class ProgressBar:
    def __init__(self, max_val: int, title: str = ""):
        self.max_val = max_val
        self.counter = 0
        self.start_time = time.time()
        self.finish_time = None
        self.title = title
        self.progress_len = 20

    def update(self, msg: str = "", just_message: bool = False):
        if not just_message:
            if self.counter < self.max_val:
                self.counter += 1

        print("\r\033[94m%s |%s>%s| %d%% | ETA: %s | %s" % (
            self.title, self.__start_len(), self.__end_len(), self.__percentage(), self.__curr_eta(), msg), end='')

    def finish(self, msg: str = ""):
        self.finish_time = time.time()
        self.counter = self.max_val
        print("\r\033[92m%s |%s>%s| %d%% | ETA: %s | %s" % (
            self.title, self.__start_len(), self.__end_len(), self.__percentage(), self.__final_eta(), msg))

    def __start_len(self):
        return '=' * int(self.counter / (self.max_val / self.progress_len))

    def __end_len(self):
        return '-' * (self.progress_len - len(self.__start_len()))

    def __curr_eta(self):
        return time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time))

    def __final_eta(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.finish_time - self.start_time))

    def __percentage(self):
        return 100 / (self.max_val / self.counter)

    def add_max_val(self, value):
        self.max_val += value
