# shortest path tracker
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.csgraph import bellman_ford

from ._linker import SLinker, calculate_num_obj_per_frame
from stracking.containers import STracks


class SNNLinker(SLinker):
    """Linker using nearest neighbor algorithm

    Find the trajectories by linking each detection to it nearest neighbor

    This tracker cannot handle split or merge events

    Example:

          particles = SParticles(...)
          euclidean_cost = EuclideanCost(max_move=5.0)
          my_tracker = SNNLinker(cost=euclidean_cost, gap=1)
          tracks = my_tracker.run(particles)


    Parameters
    ----------
    cost: SLinkerCost
        Object defining the linker cost
    gap: int
        Gap (in frame number) of possible missing detections
    min_track_length: int
        Minimum number of connections in a selected track

    """
    def __init__(self, cost=None, gap=1, min_track_length=2):
        super().__init__(cost)
        self.int_convert_coef = 10000
        self._detections = None
        self.min_track_length = min_track_length
        self.gap_closing = gap
        self.tracks_ = None
        self.track_count_ = -1
        self._dim = 0

    def run(self, particles, image=None):
        self._detections = particles.data

        self.notify('processing')
        self.progress(0)

        print('detections shape=', self._detections.shape)

        if self._detections.shape[1] == 4:
            self._dim = 3
        else:
            self._dim = 2

        # TODO implement the shortest path algorithm

        self.progress(100)
        self.notify('done')
        return STracks(data=self.tracks_, properties=None, graph={})
