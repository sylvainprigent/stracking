import numpy as np
from skimage.measure import label, regionprops

from stracking.containers import SParticles
from ._detector import SDetector


class SSegDetector(SDetector):
    """Detections from segmentation image

    Create a list of particles position from a segmentation image. The segmentation image can be a
     binary mask or a label image. This detector is useful for example to create detection from
     CellPose segmentation

    Parameters
    ----------
    is_mask: bool
        True if the input image is a mask, false if input image is a label

    """
    def __init__(self, is_mask=False):
        super().__init__()
        self.is_mask = is_mask

    def run(self, image, scale=None):
        """Run the detection on a ND image

        Parameters
        ----------
        image: ndarray
            time frames labels images
        scale: tuple or list
            scale of the image in each dimension

        Returns
        -------
        detections: SParticles

        """
        self.notify('processing')
        self.progress(0)
        if image.ndim == 3:  # 2D+t
            self.notify('processing 2D+t')
            spots_ = np.empty((0, 3))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = np.int16(image[t, :, :])
                if self.is_mask:
                    frame = label(frame, background=0)
                props = regionprops(frame)
                centroids = np.zeros((len(props), 3))  # [T, Y, X]
                for i, prop in enumerate(props):
                    centroids[i, 0] = t
                    centroids[i, 1] = prop.centroid[0]
                    centroids[i, 2] = prop.centroid[1]
                if centroids.shape[0] > 0:
                    spots_ = np.concatenate((spots_, centroids), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={}, scale=scale)
        elif image.ndim == 4:  # 3D+t
            self.notify('processing 3D+t')
            spots_ = np.empty((0, 4))
            for t in range(image.shape[0]):
                self.progress(int(100 * t / image.shape[0]))
                frame = np.int16(image[t, :, :, :])
                if self.is_mask:
                    frame = label(frame, background=0)
                props = regionprops(frame)
                centroids = np.zeros((len(props), 4))  # [T, Z, Y, X]
                for i, prop in enumerate(props):
                    centroids[i, 0] = t
                    centroids[i, 1] = prop.centroid[0]
                    centroids[i, 2] = prop.centroid[1]
                    centroids[i, 3] = prop.centroid[2]
                if centroids.shape[0] > 0:
                    spots_ = np.concatenate((spots_, centroids), axis=0)
            self.notify('done')
            self.progress(100)
            return SParticles(data=spots_, properties={}, scale=scale)
        else:
            raise Exception('SSegDetector: can process only 2D+t or 3D+t images')
