import numpy as np
import xml.etree.ElementTree as ET

from ._io import STrackIO
from stracking.containers import STracks


class ICYIO(STrackIO):
    """Read a TrackMate model

    Parameters
    ----------
    file_path: str
        Path of the xml ICY file

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
                if self._root[0].tag == 'trackfile':
                    return True
        return False

    def read(self):
        root = self._tree.getroot()
        tracks = np.empty((0, 5))

        # get the trackgroup element
        idx_trackgroup = 0
        for i in range(len(root)):
            if root[i].tag == 'trackgroup':
                idx_trackgroup = i
                break

        # parse tracks
        ids_map = {}
        graph = {}
        track_id = -1
        for track_element in root[idx_trackgroup]:
            track_id += 1
            ids_map[track_element.attrib['id']] = track_id
            for detection_element in track_element:
                row = [float(track_id),
                       float(detection_element.attrib['t']),
                       float(detection_element.attrib['z']),
                       float(detection_element.attrib['y']),
                       float(detection_element.attrib['x'])
                       ]
                tracks = np.concatenate((tracks, [row]), axis=0)

        # parse linklist
        idx_linklist = 0
        for i in range(len(root)):
            if root[i].tag == 'linklist':
                idx_linklist = i
                break

        # print("id map=", ids_map)
        for link_element in root[idx_linklist]:
            from_idx = ids_map[link_element.attrib['from']]
            to_idx = ids_map[link_element.attrib['to']]
            if to_idx in graph:
                graph[float(to_idx)].append(float(from_idx))
            else:
                graph[float(to_idx)] = [float(from_idx)]

        self.stracks = STracks(data=tracks, properties=None, graph=graph)

    def write(self):
        raise Exception('STracking cannot write to ICY XML. Please use st.json')
