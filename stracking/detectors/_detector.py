from stracking.observers import SObservable


class SDetector(SObservable):
    """Interface for a particle detector

    The parameters must be set to the constructor and the image data to the
    run method
    Example:
          ```
          my_detector = MyParticleDetector(threshold=12.0)
          particles = my_detector.run(image)
          ```

    """
    def __init__(self):
        super().__init__()

    def run(self, image, scale=None):
        """Run the detection on a ND image

        Parameters
        ----------
        image: ndarray
            time frames to analyse
        scale: tuple or list
            scale of the image in each dimension    

        Returns
        -------
        detections: SParticles

        """
        raise Exception('SDetector is abstract')
