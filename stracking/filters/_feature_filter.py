import numpy as np
from ._filter import STracksFilter


class FeatureFilter(STracksFilter):
    """Select trajectories based on feature

    This filter select trajectories where a given feature have a value between
    a given min and max value

    Parameters
    ----------
    feature_name: str
        Name of the feature to use
    min_val: float
        Minimum value of the feature to keep the track
    max_val: float
        Maximum value of the feature to keep the track

    """
    def __init__(self, feature_name, min_val, max_val):
        super().__init__()
        self.feature_name = feature_name
        self.min_val = min_val
        self.max_val = max_val

    def run(self, stracks):
        if self.feature_name not in stracks.features:
            raise Exception('FeatureFilter: feature ' + self.feature_name +
                            ' not found')
        self.notify('processing')
        self.progress(0)
        tracks_feature = stracks.features[self.feature_name]
        graph = stracks.graph
        keys = graph.keys()
        t = -1
        tracks_feature_keys = tracks_feature.keys()
        for track_id in tracks_feature_keys:
            t += 1
            self.progress(int(100*t/len(tracks_feature_keys)))
            val = tracks_feature[track_id]
            if val < self.min_val or val > self.max_val:
                # remove from data
                stracks.data = np.delete(stracks.data,
                                         stracks.data[:, 0] == track_id,
                                         axis=0)
                # remove from the graph
                if track_id in keys:
                    graph.pop(track_id)
                for key in graph.keys():
                    if track_id in graph[key]:
                        graph[key].remove(track_id)
                # TODO remove track from features
        self.notify('done')
        self.progress(100)
        return stracks

