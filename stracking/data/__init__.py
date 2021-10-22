import os.path as osp
import os
import numpy as np

__all__ = ['fake_tracks1', 'fake_tracks1_3d']

legacy_data_dir = osp.abspath(osp.dirname(__file__))


def _fetch(data_filename):
    """Fetch a given data file from the local data dir.

    This function provides the path location of the data file given
    its name in the scikit-image repository.

    Parameters
    ----------
    data_filename:
        Name of the file in the scikit-bioimaging data dir

    Returns
    -------
    Path of the local file as a python string.
    """

    filepath = os.path.join(legacy_data_dir, data_filename)

    if os.path.isfile(filepath):
        return filepath
    else:
        raise FileExistsError("Cannot find the file:", filepath)


def _load(f):
    """Load an image file located in the data directory.
    Parameters
    ----------
    f : string
        File name.
    Returns
    -------
    img : ndarray
        Image loaded from ``skimage.data_dir``.
    """
    # importing io is quite slow since it scans all the backends
    # we lazy import it here
    from skimage.io import imread
    return imread(_fetch(f))


def fake_tracks1():
    """2D+t particles moving horizontally.

    Returns
    -------
    fake_traks1 : (119, 101, 5) float ndarray
        Moving points in 2D.
    """

    return _load("fake_tracks1.tif")


def fake_tracks1_3d():
    """3D+t particles moving simultaneously.

    Returns
    -------
    fake_tracks1_3d: (5, 64, 128, 128) float ndarray
        Moving points in 3D.
    """

    f1 = _load(os.path.join('tracks1_3d', 'track1_t001.tif'))
    f2 = _load(os.path.join('tracks1_3d', 'track1_t002.tif'))
    f3 = _load(os.path.join('tracks1_3d', 'track1_t003.tif'))
    f4 = _load(os.path.join('tracks1_3d', 'track1_t004.tif'))
    f5 = _load(os.path.join('tracks1_3d', 'track1_t005.tif'))

    stack = np.stack([f1, f2, f3, f4, f5])
    return stack
