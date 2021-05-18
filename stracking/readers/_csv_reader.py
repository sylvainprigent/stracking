import numpy as np
import pandas as pd

from ._reader import STrackReaderInterface
from stracking.containers import STracks


class CSVReader(STrackReaderInterface):
    """Read a TrackMate model

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

    def parse(self):
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

        # TODO: parse attributes

        self.stracks = STracks(data=tracks, properties=None, graph={})
