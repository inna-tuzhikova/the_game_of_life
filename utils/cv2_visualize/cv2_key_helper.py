from enum import IntEnum

import cv2
import numpy as np

__all__ = ['Key']


class Key(IntEnum):
    ESC = 27
    SPACE = 32
    Q = 81
    q = 113
    LEFT = 81
    RIGHT = 83
    UP = 82
    DOWN = 84


if __name__ == '__main__':
    pass
    # cv2.imshow('', np.random.randint(10, size=(10, 10, 3), dtype=np.uint8))
    # while True:
    #     print(cv2.waitKey(0))