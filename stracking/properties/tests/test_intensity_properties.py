import numpy as np

from stracking.data import fake_tracks1
from stracking.containers import SParticles
from stracking.properties import IntensityProperty


def test_intensity_properties():
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

    property_calc = IntensityProperty(radius=2)
    property_calc.run(particles, image)

    expected_properties = {'mean_intensity': np.array(
        [246.66666667, 225.55555556, 191., 198.88888889,
         183.88888889, 161.33333333, 201.33333333, 206.77777778,
         184.11111111, 222.88888889, 244.77777778, 235.77777778,
         239., 214.66666667, 217.88888889]),
                           'std_intensity': np.array(
        [15.88850038, 38.11710351, 49.62302333, 50.52489913, 80.90521813,
         74.7217059, 49.21833443, 58.63593471, 68.99668985, 46.04453024,
         15.28090877, 25.10766938, 33.30999183, 37.13339318, 39.41642197]),
                           'min_intensity': np.array(
                               [204., 142., 103., 106., 39., 62., 94., 84., 40.,
                                111., 214.,
                                186., 152., 141., 149.]),
                           'max_intensity': np.array(
                               [255., 255., 255., 255., 255., 255., 255., 255.,
                                255., 255., 255.,
                                255., 255., 255., 255.]), 'radius': np.array(
            [2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2.])}

    np.testing.assert_almost_equal(expected_properties['mean_intensity'],
                                   particles.properties['mean_intensity'],
                                   decimal=5)
    np.testing.assert_almost_equal(expected_properties['std_intensity'],
                                   particles.properties['std_intensity'],
                                   decimal=5)
    np.testing.assert_almost_equal(expected_properties['min_intensity'],
                                   particles.properties['min_intensity'],
                                   decimal=5)
    np.testing.assert_almost_equal(expected_properties['max_intensity'],
                                   particles.properties['max_intensity'],
                                   decimal=5)
