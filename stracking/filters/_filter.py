from stracking.containers import STracks


class STracksFilter:
    """Interface for a tracks filter

    A filter can select tracks based on properties of features
    Must implement the filter method

    """
    def __init__(self):
        pass

    def run(self, stracks):
        """Run the filtering

        Parameters
        ----------
        stracks: STracks
            Tracks to filter

        Returns
        -------
        stracks: STracks
            Filtered tracks

        """
        raise Exception("STracksFilter is abstract class")
