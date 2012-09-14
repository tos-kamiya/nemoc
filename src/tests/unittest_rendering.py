#coding: utf-8

import sys
sys.path.append("..")

import unittest
import re
import nemoc


class RendringTest(unittest.TestCase):
    def testHelloWorld(self):
        rendered = nemoc.render(u"""
% ul
    %li
        Hello, World!
""")
        r = re.sub(u'[ \f\r\t\n]+', u'', rendered)
        self.assertEqual(r, u"<ul><li>Hello,World!</li></ul>")

    def testRenderWithParams(self):
        rendered = nemoc.render(u"""
% html
  % body
    % span || Hello, ${name}!
    % span || Goodbye!
""", dict(name="John"))
        r = re.sub(u'[ \f\r\t\n]+', u'', rendered)
        self.assertEqual(r, u"<html><body><span>Hello,John!</span><span>Goodbye!</span></body></html>")


if __name__ == "__main__":
    unittest.main()