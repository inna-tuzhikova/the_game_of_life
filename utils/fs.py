import os
import glob
import shutil


__all__ = ['ensure_dir', 'rm_tmp_dir']


def ensure_dir(path, rm_on_exists=False):
    if os.path.exists(path):
        if rm_on_exists:
            try:
                shutil.rmtree(path)
            except Exception as e:
                print('Directory is already exist: %s. Unable to remove it: %s' % (path, e))
                raise e
    else:
        try:
            os.makedirs(path)
        except Exception as e:
            print('Unable to create temporary directory: %s. %s' % (path, e))
            raise e


def rm_tmp_dir(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print('Unable to remove temporary dir: %s. %s' % (path, e))
            raise e
