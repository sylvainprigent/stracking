import numpy as np
import pandas as pd

from ._io import STrackIO
from stracking.containers import STracks


class CSVIO(STrackIO):
    """Read/write tracks from/to csv file

    This format does not support split/merge events and tracks features

    Parameters
    ----------
    file_path: str
        Path of the csv file

    """
    def __init__(self, file_path):
        super().__init__(file_path)

    def is_compatible(self):
        if self.file_path.endswith('.csv'):
            return True
        return False

    def read(self):
        df = pd.read_csv(self.file_path)
        headers = list(df.columns.values)
        in_tracks = df.to_numpy()

        tracks = np.zeros((in_tracks.shape[0], 5))
        if 'TrackID' in headers:
            index = headers.index('TrackID')
            tracks[:, 0] = in_tracks[:, index]
        if 't' in headers:
            index = headers.index('t')
            tracks[:, 1] = in_tracks[:, index]
        if 'z' in headers:
            index = headers.index('z')
            tracks[:, 2] = in_tracks[:, index]
        if 'y' in headers:
            index = headers.index('y')
            tracks[:, 3] = in_tracks[:, index]
        if 'x' in headers:
            index = headers.index('x')
            tracks[:, 4] = in_tracks[:, index]

        scale = [1, 1, 1]
        if 'z' in headers:
            scale = [1, 1, 1, 1]

        default_headers = ['TrackID', 't', 'z', 'y', 'x']
        properties = {}
        for head in headers:
            if head not in default_headers:
                property_ = []
                index_head = headers.index(head)
                for i in range(in_tracks.shape[0]):
                    property_.append(in_tracks[i, index_head])
                properties[head] = property_
        self.stracks = STracks(data=tracks, properties=properties, graph={}, scale=scale)

    def write(self, tracks):
        self.stracks = tracks
        # write tracks
        columns = ['TrackID', 't', 'y', 'x']
        if tracks.data.shape[1] == 5:
            columns = ['TrackID', 't', 'z', 'y', 'x']
        df = pd.DataFrame(data=tracks.data, index=None, columns=columns)
        # write properties
        for key, value in tracks.properties.items():
            df[key] = value
        print(df)
        df.to_csv(self.file_path, index=False)
