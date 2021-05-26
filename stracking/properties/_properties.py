from stracking.observers import SObservable


class SProperty(SObservable):
    """Interface to implement a property measure

    Measure a property for each particle in a SParticles

    """
    def __init__(self):
        super().__init__()

    def run(self, sparticles, image):
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
        raise Exception('SProperty is abstract')
