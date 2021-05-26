import xml.etree.ElementTree as ET
import numpy as np

from ._io import STrackIO
from stracking.containers import STracks


class TrackMateIO(STrackIO):
    """Read a TrackMate model

    Parameters
    ----------
    file_path: str
        Path of the xml TrackMate model file

    """

    def __init__(self, file_path):
        super().__init__(file_path)
        # read xml into tree
        if file_path.endswith('.xml'):
            self._tree = ET.parse(file_path)
            self._root = self._tree.getroot()
        else:
            self._root = None

        # internal tmp data
        self._tracks = None
        self._graph = {}
        self._properties = dict()
        self._features = dict()
        self._model_idx = 0
        self._track_ids_count = -1
        self._starting_sources = []
        self._starting_track_idx = []
        self._feature_tags = []
        self.init_features()
        self._props = []
        self.init_properties()

    def init_properties(self):
        self._props = ['QUALITY',
                       'MAX_INTENSITY',
                       'MEDIAN_INTENSITY',
                       'VISIBILITY',
                       'MEAN_INTENSITY',
                       'TOTAL_INTENSITY',
                       'ESTIMATED_DIAMETER',
                       'RADIUS',
                       'SNR',
                       'STANDARD_DEVIATION',
                       'CONTRAST',
                       'MANUAL_COLOR',
                       'MIN_INTENSITY']

        for prop in self._props:
            self._properties[prop] = []

    def init_features(self):
        self._feature_tags = ['NUMBER_SPOTS',
                        'NUMBER_GAPS',
                        'LONGEST_GAP',
                        'TRACK_DURATION',
                        'TRACK_START',
                        'TRACK_STOP',
                        'TRACK_DISPLACEMENT',
                        'TRACK_X_LOCATION',
                        'TRACK_Y_LOCATION',
                        'TRACK_Z_LOCATION',
                        'TRACK_MEAN_SPEED',
                        'TRACK_MAX_SPEED',
                        'TRACK_MIN_SPEED',
                        'TRACK_MEDIAN_SPEED',
                        'TRACK_STD_SPEED',
                        'TRACK_MEAN_QUALITY',
                        'TRACK_MAX_QUALITY',
                        'TRACK_MIN_QUALITY',
                        'TRACK_MEDIAN_QUALITY',
                        'TRACK_STD_QUALITY']

        for tag in self._feature_tags:
            self._features[tag] = dict()

    def _add_property(self, prop):
        for key in prop:
            if key in self._properties:
                self._properties[key].append(prop[key])

    def is_compatible(self):
        if self._root and self._root.tag == 'TrackMate':
            return True
        return False

    def read(self):
        self._tracks = np.empty((0, 5))
        # find model element
        for i in range(len(self._root)):
            if self._root[i].tag == 'Model':
                self._model_idx = i
                break
        # parse each track
        for filtered_track in self._root[self._model_idx][3]:
            # get the edges of each filtered tracks
            track_id = int(filtered_track.attrib['TRACK_ID'])
            for all_track in self._root[self._model_idx][2]:
                if int(all_track.attrib['TRACK_ID']) == track_id:
                    # if track_id == 0:  # remove later
                    self.get_track_edges(track_id, all_track)
        self.stracks = STracks(data=self._tracks, properties=self._properties,
                               graph=self._graph, features=self._features)

    def get_track_features(self, track_id, xml_element):
        for tag in self._feature_tags:
            if tag in xml_element.attrib:
                self._features[tag][track_id] = float(xml_element.attrib[tag])

    def get_track_edges(self, track_id, xml_element):
        sources = []
        targets = []
        sources_props = []
        targets_props = []
        for child in xml_element:
            source_spot, source_props = \
                self.find_spot(child.attrib['SPOT_SOURCE_ID'])
            target_spot, target_props = \
                self.find_spot(child.attrib['SPOT_TARGET_ID'])
            sources.append(source_spot)
            targets.append(target_spot)
            sources_props.append(source_props)
            targets_props.append(target_props)

        sources = np.array(sources)
        targets = np.array(targets)

        # sort sources and targets
        sort_idxs = sources[:, 1].argsort()
        sources = sources[sort_idxs]
        targets = targets[sort_idxs]
        #sources_props = sources_props[sort_idxs]
        #targets_props = targets_props[sort_idxs]

        # search for splits ids
        unique, counts = np.unique(sources[:, 0], return_counts=True)
        split_idxs = unique[np.where(counts > 1)]

        # search merge ids
        uniquet, countst = np.unique(targets[:, 0], return_counts=True)
        merge_idxs = uniquet[np.where(countst > 1)]

        self._track_ids_count += 1
        self.extract_subtrack(sources, sources_props, targets, targets_props,
                              sort_idxs, split_idxs, merge_idxs,
                              sources[0, 0], self._track_ids_count)
        self.get_track_features(self._track_ids_count, xml_element)

    def extract_subtrack(self, sources, sources_props, targets, targets_props,
                         sort_idxs, split_idxs, merge_idxs, source_id,
                         track_id):

        self._starting_sources.append(source_id)
        self._starting_track_idx.append(track_id)
        idx = np.where(sources[:, 0] == source_id)[0][0]

        # create new track
        # add sources
        source = sources[idx, :].copy()

        source[0] = track_id
        self._tracks = np.concatenate((self._tracks, [source]), axis=0)
        self._add_property(sources_props[sort_idxs[idx]])
        # add next targets
        while 1:
            source = sources[idx, :].copy()
            target = targets[idx, :].copy()
            if source[0] in split_idxs:
                # maybe need to start in the next point
                split_sources = np.where(sources[:, 0] == source[0])[0]
                for ss_id in split_sources:
                    self._track_ids_count += 1
                    next_track_id = self._track_ids_count
                    self._graph[next_track_id] = track_id
                    next_idx = targets[ss_id, 0].copy()
                    self.extract_subtrack(sources, sources_props, targets,
                                          targets_props, sort_idxs, split_idxs,
                                          merge_idxs, next_idx, next_track_id)
                break
            elif target[0] in merge_idxs:
                starting_points = np.where(sources[:, 0] == target[0])
                for sp_idx in starting_points[0]:
                    if sources[sp_idx, 0] not in self._starting_sources:
                        self._track_ids_count += 1
                        next_track_id = self._track_ids_count
                        self._graph[next_track_id] = [track_id]

                        self.extract_subtrack(sources, sources_props, targets,
                                              targets_props, sort_idxs,
                                              split_idxs, merge_idxs,
                                              sources[sp_idx, 0], next_track_id)
                    else:
                        ind = self._starting_sources.index(sources[sp_idx, 0])
                        merge_id = self._starting_track_idx[ind]
                        if merge_id in self._graph:
                            self._graph[merge_id].append(track_id)
                        else:
                            self._graph[merge_id] = [track_id]
                break
            else:
                target[0] = track_id
                self._tracks = np.concatenate((self._tracks, [target]), axis=0)
                self._add_property(targets_props[sort_idxs[idx]])

            # go to the next
            idx = np.where(sources[:, 0] == targets[idx, 0])[0]
            if len(idx) > 0:
                idx = idx[0]
            else:
                break

        self.stracks = STracks(data=self._tracks, properties=None,
                               graph=self._graph)

    def extract_spot_properties(self, spot_element):
        spot_properties = dict()
        for prop in self._props:
            if prop in spot_element.attrib:
                spot_properties[prop] = float(spot_element.attrib[prop])
        return spot_properties

    def find_spot(self, spot_id):
        all_spots = self._root[self._model_idx][1]
        for spot_in_frame in all_spots:
            for spot in spot_in_frame:
                if spot.attrib['ID'] == spot_id:
                    props = self.extract_spot_properties(spot)
                    return [int(spot_id),
                            float(spot.attrib['POSITION_T']),
                            float(spot.attrib['POSITION_Z']),
                            float(spot.attrib['POSITION_Y']),
                            float(spot.attrib['POSITION_X'])], props

    def write(self):
        raise Exception('STracking cannot write to TrackMate XML. '
                        'Please use st.json')
