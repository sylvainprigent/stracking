import numpy as np

from stracking.containers import STracks
from stracking.features import DistanceFeature
from stracking.filters import FeatureFilter


def test_length_feature():
    # init tracks
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

    tracks = STracks(data=data)

    # calculate length features
    feature_calc = DistanceFeature()
    tracks = feature_calc.run(tracks)

    # filter int
    f_filter = FeatureFilter(feature_name='distance', min_val=0, max_val=60)
    tracks = f_filter.run(tracks)

    expected_data = np.array([[0, 0, 20, 20],
                              [0, 1, 20, 35],
                              [0, 2, 20, 50],
                              [0, 3, 20, 65],
                              [0, 4, 20, 80],
                              [1, 0, 100, 25],
                              [1, 1, 100, 35],
                              [1, 2, 100, 50],
                              [1, 3, 100, 65],
                              [1, 4, 100, 80]])

    np.testing.assert_almost_equal(expected_data, tracks.data, decimal=1)
