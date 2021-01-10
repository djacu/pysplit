'''Timer is a class that behaves like a stop watch with splits.'''

import time


class Timer:
    def __init__(self):
        self._start_time = 0
        self._pause_time = 0
        self._split_list = []
        self._pause = True

    @property
    def paused(self):
        return self._pause

    @property
    def splits(self):
        return self._split_list

    def start_pause(self):
        # if not self._start_time and not self._split_list and self._pause:
        if self._pause:
            self._start_time = (self._start_time
                                + time.perf_counter_ns()
                                - self._pause_time)
            self._pause = not self._pause
            print('timer unpaused')
        elif self._start_time and not self._pause:
            self._pause_time = time.perf_counter_ns()
            self._pause = not self._pause
            print('timer paused')

    def start(self):
        if self.paused:
            self.start_pause()

    def pause(self):
        if not self.paused:
            self.start_pause()

    def reset(self):
        if self.paused:
            self._start_time = 0
            self._pause_time = 0
            self._split_list = []
            self._pause = True

    def split(self):
        if not self.paused:
            self._split_list.append(self.get_formatted())

    def get(self):
        if self._pause and not self._start_time:
            return 0
        elif self._pause and self._start_time:
            return self._pause_time - self._start_time
        else:
            return time.perf_counter_ns() - self._start_time

    def get_formatted(self):
        current_time = self.get()
        remainder, nanoseconds = divmod(current_time, 10 ** 9)
        milliseconds = nanoseconds // 10 ** 6
        remainder, seconds = divmod(remainder, 60)
        hours, minutes = divmod(remainder, 60)
        return '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours,
                                                    minutes,
                                                    seconds,
                                                    milliseconds)
