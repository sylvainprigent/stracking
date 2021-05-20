import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import napari

from stracking.containers import SParticles, STracks
from stracking.linkers import SPLinker, EuclideanCost
from stracking.features import (LengthFeature, DistanceFeature,
                                DisplacementFeature)
from stracking.properties import IntensityProperty
from stracking.filters import FeatureFilter

# 2D+t image X Y T
# 3D+t image Z X Y T

image = np.transpose(io.imread('./stracking/data/fake_tracks1.tif'), (1, 2, 0))

data = np.array([[0, 0, 20, 20],
                 [0, 1, 20, 35],
                 [0, 2, 20, 50],
                 [0, 3, 20, 65],
                 [0, 4, 20, 80],
                 [1, 0, 100, 25],
                 [1, 1, 100, 35],
                 [1, 2, 100, 50],
                 [1, 3, 100, 65],
                 [1, 4, 100, 80],
                 [2, 0, 60, 19],
                 [2, 2, 65, 50],
                 [2, 3, 60, 65],
                 [2, 4, 60, 80]]
                )

tracks = STracks(data=data)

# calculate length features
feature_calc = DistanceFeature()
tracks = feature_calc.run(tracks)

print(tracks.features)

# filter int
f_filter = FeatureFilter(feature_name='distance', min_val=0, max_val=60)
tracks = f_filter.run(tracks)

print(tracks.data)
