import os
import numpy as np
from stracking.io._reader_function import read_tracks
from stracking.containers import STracks


# tmp_path is a pytest fixture
def test_reader_trackmate(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_TrackMate.xml')

    stracks = read_tracks(my_test_file)
    assert isinstance(stracks, STracks)

    data = stracks.data
    assert isinstance(data, np.ndarray)

    graph = stracks.graph
    assert isinstance(graph, dict)

    np.testing.assert_equal((200, 5), data.shape)
    np.testing.assert_equal(8, len(graph))


def test_reader_icy(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_Icy.xml')

    stracks = read_tracks(my_test_file)
    assert isinstance(stracks, STracks)

    data = stracks.data
    assert isinstance(data, np.ndarray)

    graph = stracks.graph
    assert isinstance(graph, dict)

    np.testing.assert_equal((237, 5), data.shape)
    np.testing.assert_equal(9, len(graph))


def test_reader_isbi(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'FakeTracks_ISBI.xml')

    stracks = read_tracks(my_test_file)
    assert isinstance(stracks, STracks)

    data = stracks.data
    assert isinstance(data, np.ndarray)

    graph = stracks.graph
    assert isinstance(graph, dict)

    np.testing.assert_equal((156, 5), data.shape)
    np.testing.assert_equal(0, len(graph))


def test_reader_csv(tmp_path):
    """An example of how you might test your plugin."""

    root_dir = os.path.dirname(os.path.abspath(__file__))
    my_test_file = os.path.join(root_dir, 'two_tracks.csv')

    stracks = read_tracks(my_test_file)
    assert isinstance(stracks, STracks)

    data = stracks.data
    assert isinstance(data, np.ndarray)

    graph = stracks.graph
    assert isinstance(graph, dict)

    np.testing.assert_equal((29, 5), data.shape)
    np.testing.assert_equal(0, len(graph))
