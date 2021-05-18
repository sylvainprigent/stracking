from ._csv_reader import CSVReader
from ._trackmate_reader import TrackMateReader
from ._icy_reader import ICYReader
from ._isbi_reader import ISBIReader


def read_tracks(file_path):
    """Main track reader

    This method call the first compatible reader is found

    Parameters
    ----------
    file_path: str
        Path of the track file to read

    Returns
    -------
    tracks: STracks
        Container of the trajectories

    """
    print("read tracks:", file_path)
    # CSV
    csv_reader = CSVReader(file_path)
    if csv_reader.is_compatible():
        csv_reader.parse()
        return csv_reader.stracks

    # TrackMate
    trackmate_reader = TrackMateReader(file_path)
    if trackmate_reader.is_compatible():
        trackmate_reader.parse()
        return trackmate_reader.stracks

    # ICY
    icy_reader = ICYReader(file_path)
    if icy_reader.is_compatible():
        print('is compatible ICY :', file_path)
        icy_reader.parse()
        return icy_reader.stracks

    # ICY
    isbi_reader = ISBIReader(file_path)
    if isbi_reader.is_compatible():
        print('is compatible ISBI :', file_path)
        isbi_reader.parse()
        return isbi_reader.stracks

    print('is not compatible at all :', file_path)
    return None
