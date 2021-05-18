import numpy as np
from ._feature import SFeature


class LengthFeature(SFeature):
    """Calculate track length features.

    Length is defined here as the number of point in a track

    """
    def __init__(self):
        pass

    def measure(self, stracks, image=None):
        data = stracks.data
        tracks_ids = np.unique(data[:, 0])
        length_features = dict()
        for t_id in tracks_ids:
            length_features[t_id] = np.count_nonzero(data[:, 0] == t_id)
        stracks.features['length'] = length_features
