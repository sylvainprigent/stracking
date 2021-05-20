import os
import numpy as np

from stracking.containers import SParticles
from stracking.linkers import EuclideanCost, SPLinker


def test_sp_linker():
    """An example of how you might test your plugin."""

    detections = np.array([[0., 53., 12.],
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
                           [4., 13., 71.]])
    particles = SParticles(data=detections)

    euclidean_cost = EuclideanCost(max_cost=3000)
    my_tracker = SPLinker(cost=euclidean_cost, gap=1)
    tracks = my_tracker.run(particles)

    # print(tracks.data)

    expected_output = [[0., 0., 53., 12.],
                       [0., 1., 53., 26.],
                       [0., 2., 53., 41.],
                       [0., 3., 54., 56.],
                       [0., 4., 53., 71.],
                       [1., 0., 93., 11.],
                       [1., 1., 93., 26.],
                       [1., 2., 93., 41.],
                       [1., 3., 93., 56.],
                       [1., 4., 94., 71.],
                       [2., 0., 13., 10.],
                       [2., 1., 13., 26.],
                       [2., 2., 13., 41.],
                       [2., 3., 13., 55.],
                       [2., 4., 13., 71.]]

    np.testing.assert_almost_equal(expected_output, tracks.data, decimal=1)


def test_sp_linker_gap():
    """An example of how you might test your plugin."""

    detections = np.array([[0, 20, 20],
                           [0, 60, 20],
                           [0, 100, 20],
                           [1, 20, 35],
                           [1, 100, 35],
                           [2, 20, 50],
                           [2, 60, 50],
                           [2, 100, 50],
                           [3, 20, 65],
                           [3, 60, 65],
                           [3, 100, 65],
                           [4, 20, 80],
                           [4, 60, 80],
                           [4, 100, 80]])
    particles = SParticles(data=detections)

    euclidean_cost = EuclideanCost(max_cost=3000)
    my_tracker = SPLinker(cost=euclidean_cost, gap=2)
    tracks = my_tracker.run(particles)

    # print(tracks.data)

    expected_output = np.array([[0, 0, 20, 20],
                                [0, 1, 20, 35],
                                [0, 2, 20, 50],
                                [0, 3, 20, 65],
                                [0, 4, 20, 80],
                                [1, 0, 100, 20],
                                [1, 1, 100, 35],
                                [1, 2, 100, 50],
                                [1, 3, 100, 65],
                                [1, 4, 100, 80],
                                [2, 0, 60, 20],
                                [2, 2, 60, 50],
                                [2, 3, 60, 65],
                                [2, 4, 60, 80]]
                               )

    np.testing.assert_almost_equal(expected_output, tracks.data, decimal=1)
