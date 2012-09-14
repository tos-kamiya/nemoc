#coding: utf-8

import sys
sys.path.append("..")

import unittest
import os
import re
import shutil
import subprocess
import tempfile

import nemoc

SRC_TEXT = u"""
% ul
    %li
        \\u3053\\u3093\\u306b\\u3061\\u306f\\u3001\\u4e16\\u754c\\uff01
"""

RENDERED_TEXT_WO_SPACES = u"<ul><li>\\u3053\\u3093\\u306b\\u3061\\u306f\\u3001\\u4e16\\u754c\\uff01</li></ul>"

class RendringUnicodeTest(unittest.TestCase):
    def testHelloWorldInJapanese(self):
        rendered = nemoc.render(SRC_TEXT)
        r = re.sub(u'[ \f\r\t\n]+', u'', rendered)
        self.assertEqual(r, RENDERED_TEXT_WO_SPACES)

    def testHelloWorldInJapaneseViaFile(self):
        temp_dir = tempfile.mkdtemp()
        try:
            temp_file_src = os.path.join(temp_dir, "_unittest_rendering_unicode_src.tmp")
            temp_file_dest = os.path.join(temp_dir, "_unittest_rendering_unicode_dest.tmp")

            with open(temp_file_src, "wb") as f:
                f.write(SRC_TEXT.encode('utf-8'))

            subprocess.check_call(["python", os.path.join("..", "nemoc.py"), temp_file_src, "-o", temp_file_dest])
            with open(temp_file_dest, "rb") as f:
                rendered = f.read().decode('utf-8')

            r = re.sub(u'[ \f\r\t\n]+', u'', rendered)
            self.assertEqual(r, RENDERED_TEXT_WO_SPACES)
        finally:
            shutil.rmtree(temp_dir)

    def testHelloWorldInJapaneseViaPipe(self):
        proc = subprocess.Popen(["python", os.path.join("..", "nemoc.py")],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                close_fds=True)

        stdout_data, stderr_data = proc.communicate(input=SRC_TEXT.encode('utf-8'))
        self.assertTrue(not stderr_data)
        r = re.sub(u'[ \f\r\t\n]+', u'', stdout_data)
        self.assertEqual(r, RENDERED_TEXT_WO_SPACES)


if __name__ == "__main__":
    unittest.main()