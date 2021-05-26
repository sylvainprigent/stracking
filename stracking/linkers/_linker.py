# interface for detector
import numpy as np
from stracking.observers import SObservable


class SLinkerCost:
    """Interface for a linker cost

    This calculate the cost between two particles

    """
    def __init__(self, max_cost=1000):
        self.max_cost = max_cost

    def run(self, particle1, particle2):
        """Calculate the cost of linking particle1 and particle2

        Parameters
        ----------
        particle1 : array
            First particle data (t, Y, X) for 2D, (t, Z, Y, X) for 3D
        particle2: array
            Second particle data (t, Y, X) for 2D, (t, Z, Y, X) for 3D

        Returns
        -------
        cost: float
            Link cost

        """
        raise Exception('SLinkerCost: is abstract')


class SLinker(SObservable):
    """Interface for a particle tracker

    The parameters must be set to the constructor and the image data and
    particles to the run method
    Example:
          ```
          euclidean_cost = EuclideanCost(max_move=5.0)
          my_tracker = MyParticleTracker(cost=euclidean_cost, gap=1)
          tracks = my_detector.run(image, particles)
          ```

    Parameters
    ----------
    cost: SLinkerCost
        Object defining the linker cost

    """
    def __init__(self, cost=None):
        super().__init__()
        self.cost = cost

    def run(self, particles, image=None):
        """Run the tracker

        Parameters
        ----------
        image: ndarray
            time frames to analyse
        particles: SParticles
            List of particles for each frames

        Returns
        -------
        detections: SParticles

        """
        raise Exception('STracker is abstract')


def calculate_num_obj_per_frame(detections):
    """Calculate the number of objects for each frames

    Parameters
    ----------
    detections : ndarray
        2D array where each line is an object with the following mandatory
        features: [t, z, x, y] or [t, x, y].

    Returns
    -------
    counts : ndarray
        Number of objects for each frames
    """
    first_col = detections[:, 0]
    num_index = len(np.unique(first_col))
    counts = np.zeros(num_index, dtype=int)
    for t in range(num_index):
        counts[t] = int(np.count_nonzero(first_col == t))
    return counts
