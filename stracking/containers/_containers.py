

class SParticles:
    """Container for particles

    The container have two data. The particle array (N, D+1) of the particles
    and a properties dictionnary for the features

    Parameters
    ----------
    data : array (N, D+1)
        Coordinates for N points in D+1 dimensions. ID,T,(Z),Y,X. The first
        axis is the integer ID of the track. D is either 3 or 4 for planar
        or volumetric timeseries respectively.
    properties : dict {str: array (N,)}, DataFrame
        Properties for each point. Each property should be an array of length N,
        where N is the number of points.
    scale : tuple of float
        Scale factors for the image data.

    """
    def __init__(self, data=None, properties=dict(), scale=None):
        self.data = data
        self.properties = properties
        self.scale = scale


class STracks:
    """Container for trajectories

    This container is compatible with the Napari tracks layer

    Attributes
    ----------
    data : array (N, D+1)
        Coordinates for N points in D+1 dimensions. ID,T,(Z),Y,X. The first
        axis is the integer ID of the track. D is either 3 or 4 for planar
        or volumetric timeseries respectively.
    properties : dict {str: array (N,)}, DataFrame
        Properties for each point. Each property should be an array of length N,
        where N is the number of points.
    graph : dict {int: list}
        Graph representing associations between tracks. Dictionary defines the
        mapping between a track ID and the parents of the track. This can be
        one (the track has one parent, and the parent has >=1 child) in the
        case of track splitting, or more than one (the track has multiple
        parents, but only one child) in the case of track merging.
        See examples/tracks_3d_with_graph.py
    features: dict {str: dict}
            Properties for each tracks. Each feature should be an map of
            trackID=feature. Ex: features['length'][12]=25.2
    scale : tuple of float
        Scale factors for the image data.

    """
    def __init__(self, data=None, properties=dict(),
                 graph=dict(), features=dict(),
                 scale=tuple()):
        self.data = data
        self.properties = properties
        self.graph = graph
        self.features = features
        self.scale = scale
