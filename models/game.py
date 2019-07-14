from typing import Tuple, Union

import numpy as np


class AbstractGameOfLife:
    def __init__(self, grid_size: Tuple[int, int], initial_alive_rate: float, random_seed: Union[None, int] = None):
        self.grid_size = grid_size
        self.initial_alive_rate = initial_alive_rate
        self._random_seed = random_seed
        if self._random_seed is None:
            self._random_seed = np.random.randint(0, 10**6)
        self._init_random_state()

    def run_life(self):
        raise NotImplementedError

    def _init_random_state(self):
        np.random.seed(self._random_seed)

    def get_random_seed(self):
        return self._random_seed


# TODO unit tests
if __name__ == '__main__':
    import unittest