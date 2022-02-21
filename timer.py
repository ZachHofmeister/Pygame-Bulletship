import time
from time import thread_time

class Timer:
    def __init__(self, image_list, delay=100, is_loop=True):
        self.image_list = image_list
        self.delay = delay
        self.is_loop = is_loop
        self.last_time_switched = thread_time
        self.index = 0
        self.frames = len(self.image_list)

    def next_frame(self):
        now = thread_time
        if now - self.last_time_switched > self.delay:
            self.index += 1
            if self.is_loop:
                self.index %= self.frames
            self.last_time_switched = now


    def image(self):
        self.next_frame()
        return self.image_list[self.index]