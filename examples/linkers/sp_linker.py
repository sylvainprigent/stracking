"""
Shortest Path linker example
============================

This example shows how to track particles with the shortest path linker
"""

import numpy as np
import napari

from stracking.linkers import SPLinker, EuclideanCost
from stracking.containers import SParticles, STracks
from stracking.data import fake_tracks1

# load 2D+t sample
image = fake_tracks1()

# particles list
detections = np.array([[0., 53., 12.],
                       [0., 93., 11.],
                       [0., 13., 10.],
                       [1., 53., 26.],
                       [1., 93., 26.],
                       [1., 13., 26.],
                       [2., 13., 41.],
                       [2., 93., 41.],
                       [2., 53., 41.],
                       [3., 93., 56.],
                       [3., 13., 55.],
                       [3., 54., 56.],
                       [4., 53., 71.],
                       [4., 94., 71.],
                       [4., 13., 71.]])
particles = SParticles(data=detections)

# shortest path tracking with euclidean cost
euclidean_cost = EuclideanCost(max_cost=3000)
my_tracker = SPLinker(cost=euclidean_cost, gap=1)
tracks = my_tracker.run(particles)

viewer = napari.view_image(np.transpose(image, (2, 0, 1)),
                           name='fake particles')
viewer.add_tracks(tracks.data, name='stracking')
napari.run()
