import numpy as np
from skimage.draw import disk
from ._properties import SProperty


def ball(z, x, y, radius):
    """Calculate coordinates of points inside a ball

    Parameters
    ----------
    z, x, y : double
        Center coordinate of disk.
    radius : double
        Radius of disk.

    Returns
    -------
    coords : (zz, xx, yy) tuple
        List of the coordinates (z, y, x) of the points inside the ball.
    """

    xx = []
    yy = []
    zz = []
    r1 = radius*radius
    rr = int(round(radius))
    for xo in range(int(x-rr), int(x+rr+1)):
        for yo in range(int(y - rr), int(y+rr+1)):
            for zo in range(int(z-rr), int(z+rr+1)):
                euclid = pow(x-xo, 2) + pow(y-yo, 2) + pow(z-zo, 2)
                if euclid <= r1:
                    xx.append(xo)
                    yy.append(yo)
                    zz.append(zo)

    return zz, xx, yy


class IntensityProperty(SProperty):
    """Calculate the intensity properties of the partices

    This measure adds 5 properties: mean_intensity, min_intensity, max_intensity
    std_intensity and the radius parameter

    """
    def __init__(self, radius):
        super().__init__()
        if radius <= 0:
            raise Exception('IntensityProperty: radius must be positive')
        self.radius = radius

    def run(self, sparticles, image):
        self.notify('processing')
        self.progress(0)
        if image.ndim != sparticles.data.shape[1]:
            raise Exception('IntensityProperty: image and particles dimensions'
                            'do not match')

        if image.ndim == 4:
            self.notify('done')
            self.progress(100)
            return self._measure3d(sparticles, image)
        elif image.ndim == 3:
            self.notify('done')
            self.progress(100)
            return self._measure2d(sparticles, image)
        else:
            raise Exception('IntensityProperty: can process only (3D:2D+t) or '
                            '(4D:3D+t) arrays')

    def _measure2d(self, sparticles, image):

        particles = sparticles.data
        rr, cc = disk((0, 0), self.radius)
        mean_ = np.zeros((particles.shape[0]))
        std_ = np.zeros((particles.shape[0]))
        min_ = np.zeros((particles.shape[0]))
        max_ = np.zeros((particles.shape[0]))

        for i in range(particles.shape[0]):
            self.progress(int(100*i/particles.shape[0]))
            x = int(particles[i, 2])
            y = int(particles[i, 1])
            t = int(particles[i, 0])
            # get the disk coordinates
            val = image[t, cc+y, rr+x]
            mean_[i] = np.mean(val)
            std_[i] = np.std(val)
            min_[i] = np.min(val)
            max_[i] = np.max(val)

        sparticles.properties['mean_intensity'] = mean_
        sparticles.properties['std_intensity'] = std_
        sparticles.properties['min_intensity'] = min_
        sparticles.properties['max_intensity'] = max_
        sparticles.properties['radius'] = \
            self.radius*np.ones((particles.shape[0]))
        return sparticles

    def _measure3d(self, sparticles, image):

        zz, xx, yy = ball(0, 0, 0, self.radius)
        particles = sparticles.data
        mean_ = np.zeros((particles.shape[0]))
        std_ = np.zeros((particles.shape[0]))
        min_ = np.zeros((particles.shape[0]))
        max_ = np.zeros((particles.shape[0]))

        for i in range(particles.shape[0]):
            self.progress(int(100 * i / particles.shape[0]))
            x = int(particles[i, 3])
            y = int(particles[i, 2])
            z = int(particles[i, 1])
            t = int(particles[i, 0])
            val = image[t, zz+z, yy+y, xx+x]
            mean_[i] = np.mean(val)
            std_[i] = np.std(val)
            min_[i] = np.min(val)
            max_[i] = np.max(val)

        sparticles.properties['mean_intensity'] = mean_
        sparticles.properties['std_intensity'] = std_
        sparticles.properties['min_intensity'] = min_
        sparticles.properties['max_intensity'] = max_
        sparticles.properties['radius'] = \
            self.radius * np.ones((particles.shape[0]))
        return sparticles
