"""
Length features 2D
==================

This example shows how to detect particles in 2D+t image using the LoG detector
"""

import numpy as np

from stracking.features import (LengthFeature, DistanceFeature,
                                DisplacementFeature)
from stracking.containers import STracks

# create tracks
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
tracks = STracks(data=data, features=dict())

# Length feature
feature_calc = LengthFeature()
tracks2 = feature_calc.run(tracks)

# Distance feature
feature_calc = DistanceFeature()
tracks = feature_calc.run(tracks)

# Displacement feature
feature_calc = DisplacementFeature()
tracks = feature_calc.run(tracks)

# print results
print('features:', tracks.features)
