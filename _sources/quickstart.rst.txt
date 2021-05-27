Quick start
===========

This is a quick start example of how to use the **STracking** library. This section supposed you know the principles
of particles tracking. If it is not the case please refer to the
`Guide <guide>`_.

Input images
------------
Input images are 2D+t or 3D+t gray scaled images. 2D+t images are represented as numpy arrays with the following
columns ordering ``[T, Y, X]`` and 3D+t images are represented with numpy array with ``[T, Z, Y, X]`` columns ordering

First we load the image:

.. code-block:: python3

    from stracking import data

    image = data.fake_tracks1()


Particles detections
--------------------
The first step of particle tracking is to detect individual particles frame by frame.
**STracking** provides ``SDetector`` interface for particles detector. In this example we detect particles with the
*Difference of Gaussians* detector:

.. code-block:: python3

    from stracking.detectors import DoGDetector

    detector = DoGDetector(min_sigma=4, max_sigma=5, threshold=0.2)
    particles = detector.run(image)


The output ```articles`` is an instance of the ``SParticles`` container. It contains the list of particles as a numpy
array, the properties of the particles as a *dict* and the image scale as a *tuple*

Particles linking
-----------------
The second step is liking the particles to create tracks.
**STracking** provides ``SLinker`` interface to implement mulitple linking algorithms. In this quick start, we use the
*Shorted path* graph based linker, using the Euclidean distance between particles as a link cost function:

.. code-block:: python3

    from stracking.linkers import SPLinker

    euclidean_cost = EuclideanCost(max_cost=3000)
    my_tracker = SPLinker(cost=euclidean_cost, gap=1)
    tracks = my_tracker.run(particles)


The output ``tracks`` in an instance of the ``STracks`` container. It contains the list of tracks as a numpy array and
all the tracks metadata in dictionaries.

The next steps are shows the usage of ``SProperty``, ``SFeature`` and ``SFilter`` to analyse the trajectories

Particles properties
--------------------
The tracks properties module allows to calculate properties for the particles. This quickstart example
shows how to calculate the intensity properties of particles:

.. code-block:: python3

    from stracking.properties import IntensityProperty

    property_calc = IntensityProperty(radius=2)
    property_calc.run(particles, image)

All the calculated properties are saved in the properties attribute of the ``SParticles`` container

Tracks features
---------------
The tracks features allows to calculate feature of tracks like length, distance... This quickstart example shows how
to calculate the distance feature of tracks:

.. code-block:: python3

    from stracking.features import DistanceFeature

    feature_calc = DistanceFeature()
    feature_calc.run(tracks)

The calculated features are stored in the ``features`` attribute of the ``STracks`` container.

Tracks filter
-------------
The last module is the filter module. It allows to extract a subset of tracks base on defined criterion. In this
quickstart example, we select the tracks that move less that a distance of 60 pixels:

.. code-block:: python3

    from stracking.filters import FeatureFilter

    filter = FeatureFilter(feature_name='distance', min_val=0, max_val=60)
    filterd_tracks = filter.run(tracks)

A filter return a ``STracks`` object with the filtered set of tracks.