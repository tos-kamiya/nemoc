#coding: utf-8

import sys
sys.path.append("..")

import unittest
import doctest
import nemoc

class PydocTest(unittest.TestCase):
    def testPydoc(self):
        doctest.testsource(nemoc, "nemoc.render")


if __name__ == "__main__":
    unittest.main()