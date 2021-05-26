# interfaces
from stracking.observers import SObservable


class SFeature(SObservable):
    """Interface for a particle feature measurement

    Parameters
    ----------
    stracks: STracks
        tracks to analyse

    """
    def __init__(self):
        super().__init__()

    def run(self, stracks, image=None):
        """Measure a track property

        Parameters
        ----------
        stracks : STracks
            Track data container
        image: ndarray
            optional image data

        Returns
        -------
        stracks: STracks
            tracks with new feature

        """
        raise Exception('SFeature is abstract')
