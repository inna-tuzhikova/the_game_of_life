import os
import glob
from functools import partial

import cv2
import numpy as np

from models.game import AbstractGameOfLife
from utils.cv2_visualize.cv2_key_helper import Key


class BaseGameCaptureWrapper:
    def __init__(self, game_model: AbstractGameOfLife,
                 frame_size,
                 render_callback,
                 win_title='Game of Life',
                 **render_kwargs):
        self._game_model = game_model
        self._frame_width = frame_size[1]
        self._frame_height = frame_size[0]
        self._render_callback = partial(render_callback, **render_kwargs)
        self._win_title = win_title

    def run(self):
        raise NotImplementedError()


class VideoWrapper(BaseGameCaptureWrapper):
    def __init__(self, game_model: AbstractGameOfLife,
                 frame_size,
                 render_callback,
                 video_output_path=None,
                 video_delay: int = 10,  # ms
                 win_title='Game of Life',
                 last_frame_lasts: bool = True,
                 **render_kwargs):
        super().__init__(game_model, frame_size, render_callback, win_title, **render_kwargs)
        self._video_output_path = video_output_path
        if self._video_output_path is not None:
            self._video_delay = video_delay  # ms
            self._writer = cv2.VideoWriter(self._video_output_path,
                                           cv2.VideoWriter_fourcc(*'MPEG'),
                                           25.0,
                                           (self._frame_width, self._frame_height))
        self._video_output_path = video_output_path
        self._initial_delay = video_delay
        self._current_delay = video_delay
        self._last_frame_lasts = last_frame_lasts

    def _progressive_delay_change(self, mode: str = 'down', factor: float = .1):
        assert mode in ['up', 'down'], 'Unsupported delay change % s. Possible opts: up, down'
        self._current_delay *= (1 + factor * (1 if mode == 'up' else -1))
        func = np.ceil if mode == 'up' else np.floor
        self._current_delay = func(self._current_delay)
        self._current_delay = int(self._current_delay)
        self._current_delay = max(1, self._current_delay)

    def _fixed_delay_change(self, mode: str = 'down', factor: float = .1):
        mode = mode.lower()
        assert mode in ['up', 'down'], 'Unsupported delay change % s. Possible opts: up, down'
        step = factor * self._initial_delay
        self._current_delay += step * (1 if mode == 'up' else -1)
        func = np.ceil if mode == 'up' else np.floor
        self._current_delay = func(self._current_delay)
        self._current_delay = int(self._current_delay)
        self._current_delay = max(1, self._current_delay)

    def run(self):
        for epoch, state in self._game_model.run_life():
            frame = self._render_callback(state, epoch)
            if self._video_output_path is not None and self._writer is not None:
                self._writer.write(frame)
            cv2.imshow(self._win_title, frame)
            break_flag = False
            while True:
                key = cv2.waitKey(self._current_delay)
                # Stop running
                if key == Key.ESC:
                    break_flag = True
                    break
                # Pause
                elif key == Key.SPACE:
                    key = cv2.waitKey(0)
                    if key == Key.SPACE:
                        break
                # Slow down the video
                elif key == Key.LEFT:
                    self._progressive_delay_change('up')
                # Speed up the video
                elif key == Key.RIGHT:
                    self._progressive_delay_change('down')
                else:
                    break
            if break_flag:
                break
        if self._last_frame_lasts:
            key = cv2.waitKey(0)
            if key == Key.ESC:
                pass
        if self._video_output_path is not None and self._writer is not None:
            self._writer.release()


class SlideShowWrapper(BaseGameCaptureWrapper):
    def __init__(self, game_model: AbstractGameOfLife,
                 frame_size,
                 render_callback,
                 win_title='Game of Life',
                 **render_kwargs):
        super().__init__(game_model, frame_size, render_callback, win_title, **render_kwargs)

    def run(self):
        for epoch, state in self._game_model.run_life():
            frame = self._render_callback(state, epoch)
            cv2.imshow(self._win_title, frame)
            break_flag = False
            while True:
                key = cv2.waitKey(0)
                # Stop
                if key == Key.ESC:
                    break_flag = True
                    break
                # Next
                elif key == Key.SPACE:
                    break
                else:
                    continue
            if break_flag:
                break


# TODO unit tests
if __name__ == '__main__':
    pass
