# interfaces

class SFeature:
    """Interface for a particle feature measurement

    Parameters
    ----------
    stracks: STracks
        tracks to analyse

    """
    def __init__(self):
        pass

    def measure(self, stracks, image=None):
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