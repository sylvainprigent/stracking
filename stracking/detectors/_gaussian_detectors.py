import numpy as np
from skimage.feature import blob

from stracking.containers import SParticles
from ._detector import SDetector


class DoGDetector(SDetector):
    """Detect spots on 2D+t and 3d+t image using the DOG algorithm

    Parameters
    ----------
    min_sigma : scalar or sequence of scalars, optional
        The minimum standard deviation for Gaussian kernel. Keep this low to
        detect smaller blobs. The standard deviations of the Gaussian filter
        are given for each axis as a sequence, or as a single number, in
        which case it is equal for all axes.
    max_sigma : scalar or sequence of scalars, optional
        The maximum standard deviation for Gaussian kernel. Keep this high to
        detect larger blobs. The standard deviations of the Gaussian filter
        are given for each axis as a sequence, or as a single number, in
        which case it is equal for all axes.
    sigma_ratio : float, optional
        The ratio between the standard deviation of Gaussian Kernels used for
        computing the Difference of Gaussian
    threshold : float, optional.
        The absolute lower bound for scale space maxima. Local maxima smaller
        than thresh are ignored. Reduce this to detect blobs with less
        intensities.
    overlap : float, optional
        A value between 0 and 1. If the area of two blobs overlaps by a
        fraction greater than `threshold`, the smaller blob is eliminated.

    """
    def __init__(self, min_sigma=1, max_sigma=50, sigma_ratio=1.6,
                 threshold=2.0, overlap=.5):
        super().__init__()
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.sigma_ratio = sigma_ratio
        self.threshold = threshold
        self.overlap = overlap

    def run(self, image):
        """Run the detection on a ND image

        Parameters
        ----------
        image: ndarray
            time frames to analyse

        Returns
        -------
        detections: SParticles

        """
        self.notify('processing')
        self.progress(0)
        if image.ndim == 3:  # 2D+t
            self.notify('processing 2D+t')
            spots_ = np.empty((0, 3))
            sigma_ = np.empty((0,))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = image[t, :, :]
                blobs = blob.blob_dog(frame, self.min_sigma, self.max_sigma,
                                      self.sigma_ratio, self.threshold,
                                      self.overlap)
                spots = t*np.ones((blobs.shape[0], 3))
                spots[:, 1] = blobs[:, 0]  # x
                spots[:, 2] = blobs[:, 1]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 2]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})

        elif image.ndim == 4:  # 3D+t
            self.notify('processing 3D+t')
            spots_ = np.empty((0, 4))
            sigma_ = np.empty((0, 1))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = image[t, :, :, :]
                blobs = blob.blob_dog(frame, self.min_sigma, self.max_sigma,
                                      self.sigma_ratio, self.threshold,
                                      self.overlap)
                spots = t * np.ones((blobs.shape[0], 4))
                spots[:, 1] = blobs[:, 0]  # z
                spots[:, 2] = blobs[:, 1]  # x
                spots[:, 3] = blobs[:, 2]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 3]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})
        else:
            raise Exception('DoGDetector: can process only 2D+t or 3D+t images')


class LoGDetector(SDetector):
    """Laplacian of Gaussian spots detector

    Detect blobs on an image using the Difference of Gaussian method. The
    implementation is from scikit-image

    Parameters
    ----------
    min_sigma : scalar or sequence of scalars, optional
        the minimum standard deviation for Gaussian kernel. Keep this low to
        detect smaller blobs. The standard deviations of the Gaussian filter
        are given for each axis as a sequence, or as a single number, in
        which case it is equal for all axes.
    max_sigma : scalar or sequence of scalars, optional
        The maximum standard deviation for Gaussian kernel. Keep this high to
        detect larger blobs. The standard deviations of the Gaussian filter
        are given for each axis as a sequence, or as a single number, in
        which case it is equal for all axes.
    num_sigma : int, optional
        The number of intermediate values of standard deviations to consider
        between `min_sigma` and `max_sigma`.
    threshold : float, optional.
        The absolute lower bound for scale space maxima. Local maxima smaller
        than thresh are ignored. Reduce this to detect blobs with less
        intensities.
    overlap : float, optional
        A value between 0 and 1. If the area of two blobs overlaps by a
        fraction greater than `threshold`, the smaller blob is eliminated.
    log_scale : bool, optional
        If set intermediate values of standard deviations are interpolated
        using a logarithmic scale to the base `10`. If not, linear
        interpolation is used.
    """

    def __init__(self, min_sigma=1, max_sigma=50, num_sigma=10, threshold=.2,
                 overlap=.5, log_scale=False):
        super().__init__()
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.num_sigma = num_sigma
        self.threshold = threshold
        self.overlap = overlap
        self.log_scale = log_scale

    def run(self, image):
        """Run the detection on a ND image

        Parameters
        ----------
        image: ndarray
            time frames to analyse

        Returns
        -------
        detections: SParticles

        """
        self.notify('processing')
        self.progress(0)
        if image.ndim == 3:  # 2D+t
            self.notify('processing 2D+t')
            spots_ = np.empty((0, 3))
            sigma_ = np.empty((0,))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = image[t, :, :]
                blobs = blob.blob_log(frame, self.min_sigma,
                                      self.max_sigma,
                                      self.num_sigma, self.threshold,
                                      self.overlap, self.log_scale)
                spots = t*np.ones((blobs.shape[0], 3))
                spots[:, 1] = blobs[:, 0]  # x
                spots[:, 2] = blobs[:, 1]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 2]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})

        elif image.ndim == 4:  # 3D+t
            self.notify('processing 3D+t')
            spots_ = np.empty((0, 4))
            sigma_ = np.empty((0, 1))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = image[t, :, :, :]
                blobs = blob.blob_log(frame, self.min_sigma,
                                      self.max_sigma,
                                      self.num_sigma, self.threshold,
                                      self.overlap, self.log_scale)
                spots = t * np.ones((blobs.shape[0], 4))
                spots[:, 1] = blobs[:, 0]  # z
                spots[:, 2] = blobs[:, 1]  # x
                spots[:, 3] = blobs[:, 2]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 3]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})
        else:
            raise Exception('LoGDetector: can process only 2D+t or 3D+t images')


class DoHDetector(SDetector):
    """Determinant of Hessian spots detector.

    Implementation from scikit-image
    Blobs are found using the Determinant of Hessian method . For each blob
    found, the method returns its coordinates and the standard deviation
    of the Gaussian Kernel used for the Hessian matrix whose determinant
    detected the blob.

    Parameters
    ----------
    min_sigma : float, optional
        The minimum standard deviation for Gaussian Kernel used to compute
        Hessian matrix. Keep this low to detect smaller blobs.
    max_sigma : float, optional
        The maximum standard deviation for Gaussian Kernel used to compute
        Hessian matrix. Keep this high to detect larger blobs.
    num_sigma : int, optional
        The number of intermediate values of standard deviations to consider
        between `min_sigma` and `max_sigma`.
    threshold : float, optional.
        The absolute lower bound for scale space maxima. Local maxima smaller
        than thresh are ignored. Reduce this to detect less prominent blobs.
    overlap : float, optional
        A value between 0 and 1. If the area of two blobs overlaps by a
        fraction greater than `threshold`, the smaller blob is eliminated.
    log_scale : bool, optional
        If set intermediate values of standard deviations are interpolated
        using a logarithmic scale to the base `10`. If not, linear
        interpolation is used.

    """

    def __init__(self, min_sigma=1, max_sigma=30, num_sigma=10, threshold=0.01,
                 overlap=.5, log_scale=False):
        super().__init__()
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.num_sigma = num_sigma
        self.threshold = threshold
        self.overlap = overlap
        self.log_scale = log_scale

    def run(self, image):
        """Run the detection on a ND image

        Parameters
        ----------
        image: ndarray
            time frames to analyse

        Returns
        -------
        detections: SParticles

        """
        self.notify('processing')
        self.progress(0)
        if image.ndim == 3:  # 2D+t
            self.notify('processing 2D+t')
            spots_ = np.empty((0, 3))
            sigma_ = np.empty((0,))
            for t in range(image.shape[0]):
                self.progress(int(100*t/image.shape[0]))
                frame = image[t, :, :]
                blobs = blob.blob_doh(frame, self.min_sigma,
                                      self.max_sigma,
                                      self.num_sigma, self.threshold,
                                      self.overlap, self.log_scale)
                spots = t*np.ones((blobs.shape[0], 3))
                spots[:, 1] = blobs[:, 0]  # x
                spots[:, 2] = blobs[:, 1]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 2]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})

        elif image.ndim == 4:  # 3D+t
            self.notify('processing 3D+t')
            spots_ = np.empty((0, 4))
            sigma_ = np.empty((0, 1))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = image[t, :, :, :]
                blobs = blob.blob_doh(frame, self.min_sigma,
                                      self.max_sigma,
                                      self.num_sigma, self.threshold,
                                      self.overlap, self.log_scale)
                spots = t * np.ones((blobs.shape[0], 4))
                spots[:, 1] = blobs[:, 0]  # z
                spots[:, 2] = blobs[:, 1]  # x
                spots[:, 3] = blobs[:, 2]  # y

                spots_ = np.concatenate((spots_, spots), axis=0)
                sigma_ = np.concatenate((sigma_, blobs[:, 3]), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={'radius': sigma_})
        else:
            raise Exception('DoHDetector: can process only 2D+t or 3D+t images')
