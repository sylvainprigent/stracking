# shortest path tracker
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.csgraph import bellman_ford

from ._linker import SLinker, calculate_num_obj_per_frame
from stracking.containers import STracks


class SPLinker(SLinker):
    """Linker using Shortest Path algorithm

    Find the optimal trajectories by finding iteratively the shortest path in
    the graph of all the possible trajectories

    This tracker cannot handle split or merge events

    Example:

          particles = SParticles(...)
          euclidean_cost = EuclideanCost(max_move=5.0)
          my_tracker = SPLinker(cost=euclidean_cost, gap=1)
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
        self._jumpEpsilon = 0.01
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
        # get the number of objects per frames
        num_obj_per_frame = calculate_num_obj_per_frame(self._detections)
        detections_num = self._detections.shape[0]

        # 1- build the graph
        self.notify('processing: build graph')
        graph = lil_matrix((detections_num + 2, detections_num + 2))
        source_idx = 0
        target_idx = detections_num + 1

        # 1.1- connect source to each detection and then to target
        for i in range(detections_num):
            graph[source_idx, i + 1] = 1
            graph[i + 1, target_idx] = 1

        # 1.2- connect detections that are close enough
        num_frames = len(num_obj_per_frame)
        print('num frames=', num_frames)
        for frame in range(num_frames - 1):
            for nframe in range(1, self.gap_closing + 1):
                n_frame = frame + nframe
                if n_frame >= num_frames:
                    break
                for nt in range(num_obj_per_frame[frame]):
                    for nnt in range(num_obj_per_frame[n_frame]):

                        idx_obj1 = nt + num_obj_per_frame[0:frame].sum() + 1
                        idx_obj2 = nnt + num_obj_per_frame[0:n_frame].sum() + 1

                        cost_value = \
                            self.cost.run(self._detections[idx_obj1 - 1, :],
                                          self._detections[idx_obj2 - 1, :])

                        print('cost=', cost_value)
                        print('self.cost.max_cost=', self.cost.max_cost)
                        if cost_value < self.cost.max_cost:
                            if frame - n_frame - 1 > 0:
                                graph[idx_obj1, idx_obj2] = \
                                    int((cost_value / self.cost.max_cost - 1.0
                                         - (frame - n_frame - 1)
                                         + self._jumpEpsilon)
                                        * self.int_convert_coef)
                            else:
                                graph[idx_obj1, idx_obj2] = \
                                    int((cost_value / self.cost.max_cost - 1.0)
                                        * self.int_convert_coef)

        # 2- Optimize
        self.progress(50)
        self.notify('processing: shortest path')
        self.tracks_ = np.empty((0, self._detections.shape[1]+1))
        while 1:
            print('extract track...')
            # 2.1- Short path algorithm
            dist_matrix, predecessors = bellman_ford(csgraph=graph,
                                                     directed=True,
                                                     indices=0,
                                                     return_predecessors=True)

            # 2.2- Make track from predecessors and update graph
            track = self._path_to_track(graph, predecessors)

            if track.shape[0] <= self.min_track_length:
                break
            else:
                self.tracks_ = np.concatenate((self.tracks_, track), axis=0)

        self.progress(100)
        self.notify('done')
        return STracks(data=self.tracks_, properties=None, graph={})

    def _path_to_track(self, graph, predecessors):
        """Transform a predecessor path to a Track

        Parameters
        ----------
        graph : array
            Sparse matrix containing the graph. The track nodes are removed by
            this method
        predecessors : array
            List of the predecessors index of the objects in the path

        Returns
        -------
        track : Track
            Track object representing the estimated trajectory

        """

        track = np.empty((0, self._detections.shape[1]+1))
        current = len(predecessors) - 1
        self.track_count_ += 1
        print('dim in track to path=', self._dim)
        while 1:
            pred = predecessors[current]
            if pred > 0:
                print("add predecessor...")
                # remove the track nodes in the graph
                graph[pred, :] = 0
                graph[:, pred] = 0

                # create the track data
                object_array = self._detections[pred - 1, :]
                if self._dim == 2:
                    spot = [self.track_count_, object_array[0],
                            object_array[1], object_array[2]]
                    track = np.concatenate(([spot], track), axis=0)
                elif self._dim == 3:
                    spot = [self.track_count_, object_array[0],
                            object_array[1], object_array[2], object_array[3]]
                    track = np.concatenate(([spot], track), axis=0)
                else:
                    raise Exception('Tracker cannot create track with object'
                                    ' of dimension ' + str(self._dim))
                current = pred
            else:
                break
        return track
