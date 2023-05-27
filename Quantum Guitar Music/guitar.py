import random
import math
import time
import Quantum_randomNum
SAMPLE_RATE = 44100
DECAY_FACTOR = 0.996

class GuitarString:
    def __init__(self, frequency):
        if frequency <= 0:
            raise ValueError("Frequency must be positive.")
        self.frequency = frequency
        self.tic_time = 0
        self.queue = [0] * int(round(SAMPLE_RATE / frequency))

    def pluck(self):
        random.seed(time.time())
        for i in range(len(self.queue)):
            self.queue[i] = random.uniform(-0.5, 0.5)

    def tic(self):
        first = self.queue[0]
        self.queue = self.queue[1:]
        second = self.queue[0]
        new_term = DECAY_FACTOR * 0.5 * (first + second)
        self.queue.append(new_term)
        self.tic_time += 1

    def sample(self):
        return self.queue[0]

    def get_time(self):
        return self.tic_time

    def get_frequency(self):
        return self.frequency