import os
import numpy as np
from skimage import io

from stracking.detectors import LoGDetector, DoGDetector, DoHDetector


# tmp_path is a pytest fixture
def test_log_detector(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'tracks1_crop.tif')

    image = io.imread(my_test_file)

    detector = LoGDetector(min_sigma=4, max_sigma=5, threshold=0.2)
    particles = detector.run(image)
    # print(particles.data)

    expected_output = [[0., 54., 12.],
                       [0., 94., 12.],
                       [0., 14., 12.],
                       [1., 55., 27.],
                       [1., 94., 27.],
                       [1., 14., 27.],
                       [2., 94., 42.],
                       [2., 54., 42.],
                       [2., 14., 42.],
                       [3., 94., 57.],
                       [3., 14., 57.],
                       [3., 54., 57.],
                       [4., 54., 72.],
                       [4., 94., 72.],
                       [4., 14., 72.]]

    np.testing.assert_equal(expected_output, particles.data)


def test_dog_detector(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'tracks1_crop.tif')

    image = io.imread(my_test_file)

    detector = DoGDetector(min_sigma=4, max_sigma=5, threshold=0.15)
    particles = detector.run(image)

    expected_output = np.array([[0., 54., 12.],
                                [0., 94., 12.],
                                [0., 14., 12.],
                                [1., 94., 27.],
                                [1., 55., 27.],
                                [1., 14., 27.],
                                [2., 94., 42.],
                                [2., 54., 42.],
                                [2., 14., 42.],
                                [3., 94., 57.],
                                [3., 14., 57.],
                                [3., 54., 57.],
                                [4., 54., 72.],
                                [4., 94., 72.],
                                [4., 14., 72.]])

    np.testing.assert_equal(particles.data.shape, expected_output.shape)


def test_doh_detector(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'tracks1_crop.tif')

    image = io.imread(my_test_file)

    detector = DoHDetector(min_sigma=4, max_sigma=5, threshold=0.015)
    particles = detector.run(image)

    expected_output = [[0., 53., 12.],
                       [0., 93., 11.],
                       [0., 13., 10.],
                       [1., 53., 26.],
                       [1., 93., 26.],
                       [1., 13., 26.],
                       [2., 13., 41.],
                       [2., 93., 41.],
                       [2., 53., 41.],
                       [3., 93., 56.],
                       [3., 13., 55.],
                       [3., 54., 56.],
                       [4., 53., 71.],
                       [4., 94., 71.],
                       [4., 13., 71.]]

    np.testing.assert_equal(expected_output, particles.data)
