""" Tests for the zip rename module """
import argparse
import glob
import os
import random
import string
import tempfile
import unittest
import zipfile

from zip_rename import build_parser, extract_rename

def generate_random_string(lenght=10):
    """ Generate random strings """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(lenght))

def read_file(fname):
    """Reads a file and closes it cleanly"""
    with open(fname) as file_:
        return file_.read()

class TestParser(unittest.TestCase):
    """Test the parser """
    def test_definition(self):
        """ Test instance creation of the parser"""
        self.assertIsInstance(build_parser(), argparse.ArgumentParser)
    def test_argument_parsing(self):
        """ Test argument parsing """
        parsed = build_parser().parse_args(['test.zip'])
        self.assertEqual(parsed.filename, 'test.zip')
        parsed = build_parser().parse_args(['test.zip', '--prefix', 'a'])
        self.assertEqual(parsed.filename, 'test.zip')
        self.assertEqual(parsed.prefix, 'a')

class TestZipRename(unittest.TestCase):
    """ Class to test zip renaming"""
    def test_extract_rename(self, num_files=8):
        """ Test extract rename """
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)
            test_zip = 'test.zip'
            with zipfile.ZipFile(test_zip, 'w') as zip_file:
                for idx in range(num_files):
                    fname = "test_{}".format(idx)
                    with open(fname, 'w') as file_:
                        file_.write(generate_random_string())
                    zip_file.write(fname)
            prefix = 't'
            extract_rename(test_zip, prefix)

            after_zip = []
            before_zip = []
            for idx in range(num_files):
                raw_file = 'test_{}'.format(idx)
                post_file = 'test/t_{}'.format(idx)
                after_zip.append(read_file(raw_file))             
                before_zip.append(read_file(post_file))
            self.assertListEqual(before_zip, after_zip)

if __name__ == "__main__":
    unittest.main()
