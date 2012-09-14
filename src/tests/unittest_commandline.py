#coding: utf-8

import sys
sys.path.append("..")

import unittest
import nemoc


class CommandlineTest(unittest.TestCase):
    def testNullCommandline(self):
        cmd = nemoc._parse_args([])
        self.assertEqual(cmd['src'], None)
        self.assertEqual(cmd['dest'], None)
        self.assertEqual(cmd['params'], {})

    def testSrc(self):
        cmd = nemoc._parse_args(["inputfile"])
        self.assertEqual(cmd['src'], "inputfile")
        self.assertEqual(cmd['dest'], None)
        self.assertEqual(cmd['params'], {})

    def testDest(self):
        cmd = nemoc._parse_args(["-o", "outputfile"])
        self.assertEqual(cmd['src'], None)
        self.assertEqual(cmd['dest'], "outputfile")
        self.assertEqual(cmd['params'], {})

        cmd = nemoc._parse_args(["-ooutputfile"])
        self.assertEqual(cmd['src'], None)
        self.assertEqual(cmd['dest'], "outputfile")
        self.assertEqual(cmd['params'], {})

    def testParams(self):
        cmd = nemoc._parse_args(["--name=John", "--family=Smith"])
        self.assertEqual(cmd['src'], None)
        self.assertEqual(cmd['dest'], None)
        self.assertEqual(cmd['params'], dict(name="John", family="Smith"))

    def testShowHelpOption(self):
        print("<!-- some messages will will shown below -->")

        try:
            nemoc._parse_args(["-h"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

        try:
            nemoc._parse_args(["--help"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

        print("\n<!-- end of messages -->")

    def testTooManyCommandlineArguments(self):
        try:
            nemoc._parse_args(["inputfile1", "inputfile2"])
        except SystemExit as e:
            self.assertTrue(e.message.startswith("too many command-line arguments"))

    def testUnknownOption(self):
        try:
            nemoc._parse_args(["-k", "hoge"])
        except SystemExit as e:
            self.assertTrue(e.message.startswith("unknown option:"))

    def testInvalidParams(self):
        try:
            nemoc._parse_args(["--novalue"])
        except SystemExit as e:
            self.assertTrue(e.message.startswith("invalid parameter."))

        try:
            nemoc._parse_args(["--key=value1=value2"])
        except SystemExit as e:
            self.assertTrue(e.message.startswith("invalid parameter."))

    def testParamKeyConfliction(self):
        try:
            nemoc._parse_args(["--k=v1", "--k=v2"])
        except SystemExit as e:
            self.assertTrue(e.message.startswith("confliction of parameter key:")) 


if __name__ == "__main__":
    unittest.main()