import numpy as np
import xml.etree.ElementTree as ET

from ._reader import STrackReaderInterface
from stracking.containers import STracks


class ISBIReader(STrackReaderInterface):
    """Read a TrackMate model

    Parameters
    ----------
    file_path: str
        Path of the xml ISBI file

    """
    def __init__(self, file_path):
        super().__init__(file_path)
        # read xml into tree
        if file_path.endswith('.xml'):
            self._tree = ET.parse(file_path)
            self._root = self._tree.getroot()
        else:
            self._root = None

    def is_compatible(self):
        if self._root and self._root.tag == 'root':
            if len(self._root) >= 1:
                if self._root[0].tag == 'TrackContestISBI2012':
                    return True
        return False

    def parse(self):
        root = self._tree.getroot()
        tracks = np.empty((0, 5))

        # get the trackgroup element
        idx_trackcontest = 0
        for i in range(len(root)):
            if root[i].tag == 'TrackContestISBI2012':
                idx_trackcontest = i
                break

        # parse tracks=particles
        track_id = -1
        for particle_element in root[idx_trackcontest]:
            track_id += 1
            for detection_element in particle_element:
                row = [float(track_id),
                       float(detection_element.attrib['t']),
                       float(detection_element.attrib['z']),
                       float(detection_element.attrib['y']),
                       float(detection_element.attrib['x'])
                       ]
                tracks = np.concatenate((tracks, [row]), axis=0)

        self.stracks = STracks(data=tracks, properties=None, graph={})
