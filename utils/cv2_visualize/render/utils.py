from typing import Union, Tuple
import cv2
import numpy as np


__all__ = ['draw_grid', 'draw_cells', 'add_padding_to_image']


# TODO fix fist/last line cells drawing
def draw_grid(image: np.ndarray, grid_size=(5, 5)):
    h, w = image.shape[:2]
    grid_step = (h // grid_size[0], w // grid_size[1])

    for i in range(0, w + 1, grid_step[1]):
        cv2.line(image, (i, 0), (i, h), color=(127, 127, 127), thickness=1, lineType=cv2.LINE_AA)
    for i in range(0, h + 1, grid_step[0]):
        cv2.line(image, (0, i), (w, i), color=(127, 127, 127), thickness=1, lineType=cv2.LINE_AA)
    return image


def draw_cells(cells: np.ndarray, image: np.ndarray):
    grid_step = (image.shape[0] // cells.shape[0], image.shape[1] // cells.shape[1])
    for cell in np.argwhere(cells):
        image = cv2.rectangle(image, (cell[1] * grid_step[1], cell[0] * grid_step[0]),
                              ((cell[1] + 1) * grid_step[1], (cell[0] + 1) * grid_step[0]), (115, 226, 170), -1)
    return image


# TODO center text layout by height with cv2.getSize function
# TODO add padding color
def add_padding_to_image(image: np.ndarray,
                         padding_height: int,
                         mode: str = 'top',
                         text: Union[None, str] = None,
                         text_color: Tuple[int, int, int] = (127, 127, 127)):
    assert isinstance(mode, str)
    mode = mode.lower()
    assert mode in ['top', 'bottom'], 'Unsupported padding type. Should be one of: top, bottom'
    if mode == 'top':
        padding_spec = ((padding_height, 0), (0, 0), (0, 0))
        if text is not None:
            text_origin = (0, padding_height - 5)  # LB after padding
    elif mode == 'bottom':
        padding_spec = ((0, padding_height), (0, 0), (0, 0))
        if text is not None:
            text_origin = (0, image.shape[0] + padding_height - 5)  # LB after padding

    image = np.pad(image, padding_spec, mode='constant', constant_values=255)
    if text is not None:
        cv2.putText(image, text, text_origin, cv2.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=text_color, thickness=1)

    return image
