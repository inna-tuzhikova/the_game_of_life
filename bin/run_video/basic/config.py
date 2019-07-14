import os

from utils.fs import ensure_dir

__all__ = ['get_config']


config = {
    'n_runs': None,  # None - infinite
    'grid_size': (100, 100),
    'initial_alive_rate': .1,
    'save_video': True,
    'video_output_dir': '_output',
    'video_output_filename': 'basic_output.avi',
    'save_gif': False,
    'render_ops': {
        'image_size': (500, 500),  # h, w
        'top_padding_height': 20,
        'top_padding_text': 'The Game of Life: basic version',
        'bottom_padding_height': 20
    }

}


def _get_rendered_image_size():
    h, w = config['render_ops']['image_size']
    top_padding, bottom_padding = list(map(lambda value: 0 if value is None else value,
                                          (config['render_ops']['top_padding_height'],
                                           config['render_ops']['bottom_padding_height'])))
    return top_padding + h + bottom_padding, w


def get_config():
    n_runs = config['n_runs']
    assert n_runs is None or (isinstance(n_runs, int) and n_runs > 0), 'n_runs is either None (infinite) or integer > 0'
    for n_px, n_cells in zip(config['render_ops']['image_size'], config['grid_size']):
        assert n_px // n_cells == n_px / n_cells
    assert isinstance(config['initial_alive_rate'], float)
    if config['save_video']:
        ensure_dir(config['video_output_dir'], rm_on_exists=False)
        config['video_output_filename'] = os.path.join(config['video_output_dir'], config['video_output_filename'])
    else:
        config['video_output_filename'] = None

    config['rendered_image_size'] = _get_rendered_image_size()

    return config
