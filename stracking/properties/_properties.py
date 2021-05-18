

class SProperty:
    """Interface to implement a property measure

    Measure a property for each particle in a SParticles

    """
    def __init__(self):
        pass

    def measure(self, sparticles, image):
        """Calculate the feature

        Parameters
        ----------
        sparticles: SParticles
            Particles list
        image: array
            2D+t or 3D+t image array

        Returns
        -------
        sparticles: SParticles
            input particles with the calculated feature added to the properties

        """
        pass
