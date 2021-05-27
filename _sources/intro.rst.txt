Introduction
============

STracking is a library for particles tracking in scientific imaging

Context
-------
STracking has been developed in the `Serpico <https://team.inria.fr/serpico/>`_ research team. The goal is to provide a
modular library to track particles in 2D+t and 3D+t microscopy images. A classical application of your team is 3D+t
endosomes tracking with Lattice LightSheet microscopy.

Library components
------------------
STracking is written in python3 and uses scipy library for data structures. STracking library is organized as a scikit
library and provides a module for each particle tracking step:

* **Containers**: ``SParticles`` and ``STracks`` containers based on ``Napari`` points and track layer data structures to store particles and tracks
* **Detectors**: define a detector interface and implementations of particle detection algorithm for 2D and 3D image sequences
* **Linkers**: define a linker interface and implementation of particle linkers (or trackers) for 2D and 3D image sequences
* **properties**: define an interface and implementations of algorithms to measure properties of particles (intensity...)
* **feature**: define an interface and implementations of algorithms to measure tracks properties (length, displacement...)
* **filters**: define an interface and implementations of algorithms to select tracks
