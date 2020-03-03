#!/usr/bin/env python
""" Functions to extract and rename zip files """
import argparse
import os
import zipfile

def build_parser():
    """ Build a parser for the command line interface """
    parser = argparse.ArgumentParser(description='A zip renamer utility')
    parser.add_argument('filename',
                        help='The zip file path')
    parser.add_argument('--prefix',
                        help='A prefix for the extracted files',
                        default='file')
    return parser
def extract_rename(zip_path, prefix):
    """ Extract and rename the file contained in the zip archive.
    Parameters:
    -----------
    zip_path: str
        Path of the zip file to extract
    prefix: str
        Prefix to prepend to the extracted files
    """
    unzip_folder = zip_path.strip('.zip')
    os.mkdir(unzip_folder)
    zip_file = zipfile.ZipFile(zip_path, mode='r')
    for idx, file_ in enumerate(zip_file.filelist):
        file_.filename = '{}_{}'.format(prefix, idx)
        zip_file.extract(file_, path=unzip_folder)

if __name__ == "__main__":
    ARGS = build_parser().parse_args()
    extract_rename(os.path.abspath(ARGS.filename), ARGS.prefix)
