Install
=======

This section contains the instructions to install ``STracking``

Using PyPI
----------

Releases are available in PyPI a repository. We recommend using virtual environment

.. code-block:: shell

    python -m venv .stracking-env
    source .stracking-env/bin/activate
    pip install stracking


From source
-----------

If you plan to develop ``STracking`` we recommend installing locally

.. code-block:: shell

    python -m venv .stracking-env
    source .stracking-env/bin/activate
    git clone https://github.com/sylvainprigent/stracking.git
    cd stracking
    pip install -e .
