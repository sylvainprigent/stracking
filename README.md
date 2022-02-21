# STracking

**STracking** is a python framework to develop particles tracking pipeline. This library has been 
developed to track intra-cellular object in microscopy 2D+t and 3D+t images, but can be use to any 
spots tracking application in 2D+t and 3D+t images.

# install

## Library installation from PyPI

1. Install an [Anaconda](https://www.anaconda.com/download/) distribution of Python -- Choose **Python 3.9** and your operating system. Note you might need to use an anaconda prompt if you did not add anaconda to the path.
2. Open an anaconda prompt / command prompt with `conda` for **python 3** in the path
3. Create a new environment with `conda create --name stracking python=3.9`.
4. To activate this new environment, run `conda activate stracking`
5. To install the `STracking`library, run `python -m pip install stracking`. 

if you need to update to a new release, use:
~~~sh
python -m pip install stracking --upgrade
~~~

## Library installation from source

This install is for developers or people who want the last features in the ``main`` branch.

1. Install an [Anaconda](https://www.anaconda.com/download/) distribution of Python -- Choose **Python 3.9** and your operating system. Note you might need to use an anaconda prompt if you did not add anaconda to the path.
2. Open an anaconda prompt / command prompt with `conda` for **python 3** in the path
3. Create a new environment with `conda create --name stracking python=3.9`.
4. To activate this new environment, run `conda activate stracking`
5. Pull the source code from git with `git pull https://github.com/sylvainprigent/stracking.git 
6. Then install the `STracking` library from you local dir with: `python -m pip install -e ./stracking`. 

## Use STracking with napari

The STracking library is embedded in a napari plugin that allows using ``STracking`` with a graphical interface.
Please refer to the [`STracking` napari plugin](https://www.napari-hub.org/plugins/napari-stracking) documentation to install and use it.

# STracking documentation

The full documentation with tutorial and docstring is available [here](https://sylvainprigent.github.io/stracking/)