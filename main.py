import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import napari

from stracking.data import fake_tracks1
from stracking.containers import SParticles, STracks
from stracking.detectors import DoGDetector, DoHDetector
from stracking.linkers import SPLinker, EuclideanCost
from stracking.features import (LengthFeature, DistanceFeature,
                                DisplacementFeature)
from stracking.properties import IntensityProperty
from stracking.filters import FeatureFilter
from stracking.io import StIO, TrackMateIO


tracks_file = '/Users/sprigent/Documents/code/napari/stracking/stracking/io/tests/FakeTracks_TrackMate.xml'

reader = TrackMateIO(tracks_file)
reader.read()
tracks = reader.stracks
print(tracks.data)
#print(tracks.features)
print(tracks.properties)

print('spot number=', tracks.data.shape[0])
print('min intensity props num=', len(tracks.properties['MIN_INTENSITY']))

# 2D+t image T X Y
# 3D+t image T Z X Y

# initialize the input data
#image = fake_tracks1()
#spots = np.array([[0., 54., 12.],
#                  [0., 94., 12.],
#                  [0., 14., 12.],
#                  [1., 55., 27.],
#                  [1., 94., 27.],
#                  [1., 14., 27.],
#                  [2., 94., 42.],
#                  [2., 54., 42.],
#                  [2., 14., 42.],
#                  [3., 94., 57.],
#                  [3., 14., 57.],
#                  [3., 54., 57.],
#                  [4., 54., 72.],
#                  [4., 94., 72.],
#                  [4., 14., 72.]])
#particles = SParticles(data=spots)

## calculate the intensity properties with a particle of radius=2
#property_calc = IntensityProperty(radius=2)
#property_calc.run(particles, image)

## show the calculated properties
#print(particles.properties)


#image = np.transpose(io.imread('./stracking/data/fake_tracks1.tif'), (1, 2, 0))

#data = np.array([[0, 0, 20, 20],
#                 [0, 1, 20, 35],
#                 [0, 2, 20, 50],
#                 [0, 3, 20, 65],
#                 [0, 4, 20, 80],
#                 [1, 0, 100, 25],
#                 [1, 1, 100, 35],
#                 [1, 2, 100, 50],
#                 [1, 3, 100, 65],
#                 [1, 4, 100, 80],
#                 [2, 0, 60, 19],
#                 [2, 2, 65, 50],
#                 [2, 3, 60, 65],
#                 [2, 4, 60, 80]]
#                )

#tracks = STracks(data=data)

## calculate length features
#feature_calc = DistanceFeature()
#tracks = feature_calc.run(tracks)

#print(tracks.features)

## save tracks
#io = StIO('sample.st.json')
#io.stracks = tracks
#io.write()

#io_read = StIO('sample.st.json')
#io.read()
#print(io.stracks.data)
#print(io.stracks.features)

# filter int
#f_filter = FeatureFilter(feature_name='distance', min_val=0, max_val=60)
#tracks = f_filter.run(tracks)

#print(tracks.data)
