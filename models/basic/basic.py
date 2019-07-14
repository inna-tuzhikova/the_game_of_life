from typing import Tuple, Union

import numpy as np
from scipy import signal
from models.game import AbstractGameOfLife


class BasicGameOfLife(AbstractGameOfLife):
    def __init__(self, grid_size: Tuple[int, int], initial_alive_rate: float, random_seed: Union[None, int] = None):
        super().__init__(grid_size, initial_alive_rate, random_seed)

    def run_life(self):
        epoch = 0
        current_state = self._get_initial_epoch()
        life_states = [current_state]
        while True:
            yield epoch, current_state
            current_state = self._get_next_epoch(current_state)
            if not self._is_a_member(current_state, life_states):
                life_states.append(current_state)
                epoch += 1
            else:
                break

    def _get_initial_epoch(self):
        initial_cells = (np.random.random(self.grid_size) < self.initial_alive_rate)
        return initial_cells.astype(np.uint8)

    def _get_num_of_neighbors(self, grid: np.ndarray):
        kernel = np.ones((3, 3), dtype=np.uint8)
        res = signal.convolve2d(grid, kernel, 'same', fillvalue=0) - grid
        return res

    def _get_next_epoch(self, cells: np.ndarray):
        neighbors = self._get_num_of_neighbors(cells)
        next_epoch = ((cells == 0) & (neighbors == 3)) |  \
                     ((cells == 1) & ((neighbors == 2) | (neighbors == 3)))
        return next_epoch

    def _is_a_member(self, other_item, np_items):
        for item in np_items:
            if np.array_equal(other_item, item):
                return True
        return False


# TODO unit.tests
if __name__ == '__main__':
    pass
