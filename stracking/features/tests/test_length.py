import numpy as np

from stracking.containers import STracks
from stracking.features import (LengthFeature, DistanceFeature,
                                DisplacementFeature)


def test_length_feature():
    data = np.array([[0, 0, 20, 20],
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

    tracks = STracks(data=data)

    feature_calc = LengthFeature()
    tracks = feature_calc.run(tracks)

    # print(tracks.data)
    # print(tracks.features)

    expected_data = np.array([[0, 0, 20, 20],
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

    expected_features = {'length': {0: 5, 1: 5, 2: 4}}

    np.testing.assert_almost_equal(expected_data, tracks.data, decimal=1)
    np.testing.assert_equal(expected_features, tracks.features)


def test_distance_feature():
    data = np.array([[0, 0, 20, 20],
                     [0, 1, 20, 35],
                     [0, 2, 20, 50],
                     [0, 3, 20, 65],
                     [0, 4, 20, 80],
                     [1, 0, 100, 25],
                     [1, 1, 100, 35],
                     [1, 2, 100, 50],
                     [1, 3, 100, 65],
                     [1, 4, 100, 80],
                     [2, 0, 60, 19],
                     [2, 2, 60, 50],
                     [2, 3, 60, 65],
                     [2, 4, 60, 80]]
                    )

    tracks2 = STracks(data=data, features=dict())

    print('features before=')
    print(tracks2.features)

    feature_calc = DistanceFeature()
    tracks2 = feature_calc.run(tracks2)

    print(tracks2.data)
    print('features=')
    print(tracks2.features)

    expected_data = np.array([[0, 0, 20, 20],
                              [0, 1, 20, 35],
                              [0, 2, 20, 50],
                              [0, 3, 20, 65],
                              [0, 4, 20, 80],
                              [1, 0, 100, 25],
                              [1, 1, 100, 35],
                              [1, 2, 100, 50],
                              [1, 3, 100, 65],
                              [1, 4, 100, 80],
                              [2, 0, 60, 19],
                              [2, 2, 60, 50],
                              [2, 3, 60, 65],
                              [2, 4, 60, 80]]
                             )

    expected_features = {'distance': {0: 60.0, 1: 55.0, 2: 61.0}}

    np.testing.assert_almost_equal(expected_data, tracks2.data, decimal=1)
    np.testing.assert_equal(expected_features, tracks2.features)


def test_displacement_feature():
    data = np.array([[0, 0, 20, 20],
                     [0, 1, 20, 35],
                     [0, 2, 20, 50],
                     [0, 3, 20, 65],
                     [0, 4, 20, 80],
                     [1, 0, 100, 25],
                     [1, 1, 100, 35],
                     [1, 2, 100, 50],
                     [1, 3, 100, 65],
                     [1, 4, 100, 80],
                     [2, 0, 60, 19],
                     [2, 2, 65, 50],
                     [2, 3, 60, 65],
                     [2, 4, 60, 80]]
                    )

    tracks2 = STracks(data=data, features=dict())

    print('features before=')
    print(tracks2.features)

    feature_calc = DisplacementFeature()
    tracks2 = feature_calc.run(tracks2)

    print(tracks2.data)
    print('features=')
    print(tracks2.features)

    expected_data = np.array([[0, 0, 20, 20],
                              [0, 1, 20, 35],
                              [0, 2, 20, 50],
                              [0, 3, 20, 65],
                              [0, 4, 20, 80],
                              [1, 0, 100, 25],
                              [1, 1, 100, 35],
                              [1, 2, 100, 50],
                              [1, 3, 100, 65],
                              [1, 4, 100, 80],
                              [2, 0, 60, 19],
                              [2, 2, 65, 50],
                              [2, 3, 60, 65],
                              [2, 4, 60, 80]]
                             )

    expected_features = {'displacement': {0: 60.0, 1: 55.0, 2: 61.0}}

    np.testing.assert_almost_equal(expected_data, tracks2.data, decimal=1)
    np.testing.assert_equal(expected_features, tracks2.features)
