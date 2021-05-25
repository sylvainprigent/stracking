# Reader interface and service

class STrackIO:
    """Interface for a tracks reader/write

    Parameters
    ----------
    file_path: str
        Path of the file to read

    Attributes
    ----------
    stracks : STracks
        Container of the read tracks

    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.stracks = None

    def is_compatible(self):
        """Check if the file format and the reader are compatible

        Returns
        -------
        compatible: bool
            True if the reader and the filter are compatible, False otherwise

        """
        return False

    def read(self):
        """Read a track file into STracks

        The parsed data are stored in the stracks attribute

        """
        raise Exception('STrackIO is abstract')

    def write(self):
        """Write tracks to file"""
        raise Exception('STrackIO is abstract')

