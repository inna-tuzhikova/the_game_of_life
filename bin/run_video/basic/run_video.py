import cv2

from models.basic.basic import BasicGameOfLife
from utils.cv2_visualize.render.game_state_renders import render_state_basic
from utils.cv2_visualize.game_capture import VideoWrapper, SlideShowWrapper
from bin.run_video.basic.config import get_config
from utils.cv2_visualize.cv2_key_helper import Key

if __name__ == '__main__':
    config = get_config()
    n_runs = config['n_runs']
    run_idx = 1
    while True:
        game_model = BasicGameOfLife(grid_size=config['grid_size'],
                                     initial_alive_rate=config['initial_alive_rate'])
        wrapper = VideoWrapper(game_model=game_model,
                               frame_size=config['rendered_image_size'],
                               render_callback=render_state_basic,
                               # video_output_path=config['video_output_filename'],
                               # video_delay=100,
                               win_title='RUN %d. The Game of Life: basic version' % run_idx,
                               # last_frame_lasts=False,
                               **config['render_ops'])
        wrapper.run()
        run_idx += 1
        if n_runs is not None:
            if run_idx > n_runs:
                break
        break_flag = False
        while True:
            key = cv2.waitKey(0)
            # Stop
            if key == Key.Q or key == Key.q:
                break_flag = True
                break
            # Next run
            elif key == Key.ESC:
                cv2.destroyAllWindows()
                break
            else:
                continue
        if break_flag:
            break
    cv2.destroyAllWindows()
