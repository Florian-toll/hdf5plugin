# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2019 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
__authors__ = ["V.A. Sole", "T. Vincent"]
__license__ = "MIT"
__date__ = "04/10/2019"


import os
import unittest

import numpy
import h5py
import hdf5plugin
from hdf5plugin.test import suite as hdf5plugin_suite


class TestHDF5PluginRead(unittest.TestCase):
    """Test reading existing files with compressed data"""

    def testBlosc(self):
        """Test reading Blosc compressed data"""
        dirname = os.path.abspath(os.path.dirname(__file__))
        # the blosc.h5 is in fact the example.h5 file generated
        # using the example.c file from the blosc respository.
        fname = os.path.join(dirname, "blosc.h5")
        self.assertTrue(os.path.exists(fname),
                        "Cannot find %s file" % fname)
        h5 = h5py.File(fname, "r")
        data = h5["/dset"][:]
        h5.close()
        expected_shape = (100, 100, 100)
        self.assertTrue(data.shape[0] == 100, "Incorrect shape")
        self.assertTrue(data.shape[1] == 100, "Incorrect shape")
        self.assertTrue(data.shape[2] == 100, "Incorrect shape")

        target = numpy.arange(numpy.prod(expected_shape),
                              dtype=numpy.float)
        target.shape = expected_shape
        self.assertTrue(numpy.allclose(data, target), "Incorrect readout")

    def testLZ4(self):
        """Test reading lz4 compressed data"""
        dirname = os.path.abspath(os.path.dirname(__file__))
        fname = os.path.join(dirname, "lz4.h5")
        self.assertTrue(os.path.exists(fname),
                        "Cannot find %s file" % fname)
        h5 = h5py.File(fname, "r")
        data = h5["/entry/data"][:]
        h5.close()
        expected_shape = (50, 2167, 2070)
        self.assertTrue(data.shape[0] == 50, "Incorrect shape")
        self.assertTrue(data.shape[1] == 2167, "Incorrect shape")
        self.assertTrue(data.shape[2] == 2070, "Incorrect shape")
        self.assertTrue(data[21, 1911, 1549] == 3141, "Incorrect value")

    def testBitshuffle(self):
        """Test reading bitshuffle compressed data"""
        dirname = os.path.abspath(os.path.dirname(__file__))
        fname = os.path.join(dirname, "bitshuffle.h5")
        self.assertTrue(os.path.exists(fname),
                        "Cannot find %s file" % fname)
        h5 = h5py.File(fname, "r")
        data = h5["/entry/data/data"][:]
        h5.close()
        expected_shape = (1, 2167, 2070)
        self.assertTrue(data.shape[0] == 1, "Incorrect shape")
        self.assertTrue(data.shape[1] == 2167, "Incorrect shape")
        self.assertTrue(data.shape[2] == 2070, "Incorrect shape")
        self.assertTrue(data[0, 1372, 613] == 922, "Incorrect value")


def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(
        TestHDF5PluginRead))
    testSuite.addTest(hdf5plugin_suite())
    return testSuite


if __name__ == "__main__":
    import sys
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
