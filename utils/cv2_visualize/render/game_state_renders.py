from typing import Union, Tuple

import cv2
import numpy as np

from utils.cv2_visualize.render.utils import draw_grid, draw_cells, add_padding_to_image

__all__ = ['render_state_basic']


def render_state_basic(state: np.ndarray,
                       epoch: int,
                       image_size: Tuple[int, int, int] = (100, 100, 3),
                       top_padding_height: Union[None, int] = None,
                       top_padding_text: Union[None, str] = None,
                       bottom_padding_height: Union[None, int] = 20):
    assert len(image_size) == 2
    canvas = 255 * np.ones((*image_size, 3), dtype=np.uint8)
    canvas = draw_cells(state, canvas)
    canvas = draw_grid(canvas, state.shape)
    if top_padding_height is not None and top_padding_height > 0:
        canvas = add_padding_to_image(image=canvas, padding_height=top_padding_height,
                                      mode='top', text=top_padding_text)
    if bottom_padding_height is not None and bottom_padding_height > 0:
        canvas = add_padding_to_image(image=canvas, padding_height=bottom_padding_height,
                                      mode='bottom', text='Epoch %d' % epoch)
    return canvas


# TODO unit tests
if __name__ == '__main__':
    pass