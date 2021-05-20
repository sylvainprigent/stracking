import numpy as np
from skimage import io
from stracking.detectors import LoGDetector, DoGDetector, DoHDetector
import matplotlib.pyplot as plt

import napari

# 2D+t image X Y T
# 3D+t image Z X Y T

detector = 'DoH'
image = io.imread('./stracking/detectors/tests/tracks1_crop.tif')
print('image shape=', image.shape)

image2 = np.transpose(image, (1, 2, 0))
print('reshaped image=', image2.shape)

#for i in range(image2.shape[2]):
#    plt.figure()
#    plt.imshow(image2[:, :, i], cmap='gray')
#plt.show()

if detector == 'LoG':
    detector = LoGDetector(min_sigma=4, max_sigma=5, threshold=0.2)
    particles = detector.run(image2)
elif detector == 'DoG':
    detector = DoGDetector(min_sigma=4, max_sigma=5, threshold=0.2)
    particles = detector.run(image2)
elif detector == 'DoH':
    detector = DoHDetector(min_sigma=4, max_sigma=5, threshold=0.015)
    particles = detector.run(image2)
print(particles.data)


print(particles.data)

viewer = napari.view_image(image)
viewer.add_points(particles.data, size=2)
napari.run()
