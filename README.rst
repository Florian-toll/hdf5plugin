hdf5plugin
==========

This module provides HDF5 compression filters (namely: blosc, bitshuffle and lz4) and registers them to the HDF5 library used by `h5py <https://www.h5py.org>`_.

Supported platforms are: Linux, Windows, macOS.

Whenever possible, HDF5 compression filter plugins are best installed system-wide or through Anaconda (`blosc-hdf5-plugin <https://anaconda.org/conda-forge/blosc-hdf5-plugin>`_, `hdf5-lz4 <https://anaconda.org/nsls2forge/hdf5-lz4>`_).
Yet, `hdf5plugin` provides a generic way to enable `h5py` with the provided HDF5 compression filters.

The HDF5 plugin sources were obtained from:

* LZ4 plugin (v0.1.0): https://github.com/nexusformat/HDF5-External-Filter-Plugins
* bitshuffle plugin (0.3.5): https://github.com/kiyo-masui/bitshuffle
* hdf5-blosc plugin (v1.0.0) and c-blosc (v1.17.0): https://github.com/Blosc/hdf5-blosc and https://github.com/Blosc/c-blosc

Installation
------------

To install, just run::

     pip install hdf5plugin

To install locally, run::

     pip install hdf5plugin --user

Documentation
-------------

To use it, just use ``import hdf5plugin`` and supported compression filters are available from `h5py <https://www.h5py.org>`_.

Sample code:

.. code-block:: python

  import numpy
  import h5py
  import hdf5plugin

  # Compression
  f = h5py.File('test.h5', 'w')
  f.create_dataset('data', data=numpy.arange(100), compression=hdf5plugin.LZ4)
  f.close()

  # Decompression
  f = h5py.File('test.h5', 'r')
  data = f['data'][()]
  f.close()

``hdf5plugin`` provides:

* The HDF5 filter ID of embedded plugins:

  - ``BLOSC``
  - ``BSHUF``
  - ``LZ4``

* Compression option helper functions to prepare arguments to provide to ``h5py.Group.create_dataset``:

  - `bitshuffle_options(nelems=0, lz4=True)`_
  - `blosc_options(level=9, shuffle='byte', compression='blosclz')`_
  - `lz4_options(nbytes=0)`_

* ``FILTERS``: A dictionary mapping provided filters to their ID
* ``PLUGINS_PATH``: The directory where the provided filters library are stored.


bitshuffle_options(nelems=0, lz4=True)
**************************************

This function takes the following arguments and returns the compression options to feed into ``h5py.Group.create_dataset`` for using the bitshuffle filter:

* **nelems** the number of elements per block, needs to be divisible by eight (default is 0, about 8kB per block)
* **lz4** if True the elements get compressed using lz4 (default is True)

It returns a dict that can be passed as keyword arguments.

Sample code:

.. code-block:: python

        f = h5py.File('test.h5', 'w')
        f.create_dataset('bitshuffle_with_lz4', data=numpy.arange(100),
	    **hdf5plugin.bshuf_options(nelems=0, lz4=True))
        f.close()


blosc_options(level=9, shuffle='byte', compression='blosclz')
*************************************************************

This function takes the following arguments and returns the compression options to feed into ``h5py.Group.create_dataset`` for using the blosc filter:

* **level** the compression level, from 0 to 9 (default is 9)
* **shuffle** the shuffling mode, either 'none', 'bit' or 'byte' (default is 'byte')
* **compression** the compressor blosc ID, one of:

  * 'blosclz' (default)
  * 'lz4'
  * 'lz4hc'
  * 'zlib'
  * 'zstd'

It returns a dict that can be passed as keyword arguments.

Sample code:

.. code-block:: python

        f = h5py.File('test.h5', 'w')
        f.create_dataset('blosc_byte_shuffle_blosclz', data=numpy.arange(100),
            **hdf5plugin.blosc_options(level=9, shuffle='byte', compression='blosclz'))
        f.close()


lz4_options(nbytes=0)
*********************

This function takes the number of bytes per block as argument and returns the compression options to feed into ``h5py.Group.create_dataset`` for using the lz4 filter:

* **nbytes** number of bytes per block needs to be in the range of 0 < nbytes < 2113929216 (1,9GB).
  The default value is 0 (for 1GB).

It returns a dict that can be passed as keyword arguments.

Sample code:

.. code-block:: python

        f = h5py.File('test.h5', 'w')
        f.create_dataset('lz4', data=numpy.arange(100),
            **hdf5plugin.lz4_options(nbytes=0)) 
        f.close()

Dependencies
------------

* `h5py <https://www.h5py.org>`_


Testing
-------

To run self-contained tests, from Python:

.. code-block:: python

  import hdf5plugin.test
  hdf5plugin.test.run_tests()

Or, from the command line::

  python -m hdf5plugin.test

To also run tests relying on actual HDF5 files, run from the source directory::

  python test/test.py

This tests the installed version of `hdf5plugin`.

License
-------

The source code of *hdf5plugin* itself is licensed under the MIT license.
Use it at your own risk.
See `LICENSE <https://github.com/silx-kit/hdf5plugin/blob/master/LICENSE>`_

The source code of the embedded HDF5 filter plugin libraries is licensed under different open-source licenses.
Please read the different licenses:

* bitshuffle: See `src/bitshuffle/LICENSE <https://github.com/silx-kit/hdf5plugin/blob/master/src/bitshuffle/LICENSE>`_
* blosc: See `src/hdf5-blosc/LICENSES/ <https://github.com/silx-kit/hdf5plugin/blob/master/src/hdf5-blosc/LICENSES/>`_ and `src/c-blosc/LICENSES/ <https://github.com/silx-kit/hdf5plugin/blob/master/src/c-blosc/LICENSES/>`_
* lz4: See `src/LZ4/COPYING  <https://github.com/silx-kit/hdf5plugin/blob/master/src/LZ4/COPYING>`_

The HDF5 v1.10.5 headers (and Windows .lib file) used to build the filters are stored for convenience in the repository. The license is available here: `src/hdf5/COPYING <https://github.com/silx-kit/hdf5plugin/blob/master/src/hdf5/COPYING>`_.
