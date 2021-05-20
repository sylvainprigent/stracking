"""
Intensity properties example
============================

This example shows how calculate intensity properties
"""

import numpy as np

from stracking.properties import IntensityProperty
from stracking.containers import SParticles, STracks
from stracking.data import fake_tracks1

# initialize the input data
image = fake_tracks1()
spots = np.array([[0., 54., 12.],
                  [0., 94., 12.],
                  [0., 14., 12.],
                  [1., 55., 27.],
                  [1., 94., 27.],
                  [1., 14., 27.],
                  [2., 94., 42.],
                  [2., 54., 42.],
                  [2., 14., 42.],
                  [3., 94., 57.],
                  [3., 14., 57.],
                  [3., 54., 57.],
                  [4., 54., 72.],
                  [4., 94., 72.],
                  [4., 14., 72.]])
particles = SParticles(data=spots)

# calculate the intensity properties with a particle of radius=2
property_calc = IntensityProperty(radius=2)
property_calc.run(particles, image)

# show the calculated properties
print(particles.properties)
