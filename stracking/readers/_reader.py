# Reader interface and service

class STrackReaderInterface:
    """Interface for a tracks reader

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

    def parse(self):
        """Parse the track file

        The parsed data are stored in the stracks attribute

        """
        raise Exception('STrackReaderInterface is abstract')
