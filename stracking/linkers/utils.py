import numpy as np


def match_properties(particles, tracks):
    """Copy properties calculated from particles to tracks

    Parameters
    ----------
    particles: SParticles
        Set of particles with properties
    tracks: STRack
        Set of track without properties

    Returns
    -------
    the set of tracks with properties

    """
    # add all the properties
    properties = {}
    for property_ in particles.properties:
        properties[property_] = []
    # fill properties
    for i in range(tracks.data.shape[0]):
        x = np.where((particles.data == tracks.data[i, 1:]).all(axis=1))
        if len(x) > 0:
            for property_ in particles.properties:
                properties[property_].append(float(particles.properties[property_][x[0]]))
    for property_ in particles.properties:
        properties[property_] = np.array(properties[property_])
    tracks.properties = properties
    return tracks
