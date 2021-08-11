Build locally
=============

do::
    python3 setup.py build_ext --inplace


Building from source
====================

Building from source is required to work on a contribution (bug fix, new
feature, code or documentation improvement).

.. _git_repo:

#. Use `Git <https://git-scm.com/>`_ to check out the latest source from the
   `stracking repository <https://github.com/sylvainprigent/stracking>`_ on
   GitLab.::

        git clone git://github.com/sylvainprigent/stracking.git  # add --depth 1 if your connection is slow
        cd stracking

   If you plan on submitting a pull-request, you should clone from your fork
   instead.

#. Install a compiler with OpenMP_ support for your platform.

#. Optional (but recommended): create and activate a dedicated virtualenv_
   or `conda environment`_.

#. Install Cython_ and build the project with pip in :ref:`editable_mode`::

        pip install cython
        pip install --verbose --no-build-isolation --editable .

#. Check that the installed scikit-learn has a version number ending with
   `.dev0`::

    python -c "import sklearn; print(sklearn.__version__)"


.. note::

    You will have to run the ``pip install --no-build-isolation --editable .``
    command every time the source code of a Cython file is updated
    (ending in `.pyx` or `.pxd`). Use the ``--no-build-isolation`` flag to
    avoid compiling the whole project each time, only the files you have
    modified.

Create a wheel
==============

do::

    python3 setup.py bdist_wheel

Testing
=======

run tests by running::

    pytest stracking

or

    python3 -m pytest stracking


Profiling
=========

python -m cProfile -o out_profile script_name.py
cprofilev -f out_profile

Build documentation
===================

without example gallery::

    cd doc
    make

with the example gallery (may take a while)::

    cd doc
    make html

