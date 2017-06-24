#!/bin/env python
"""panbib - map tlzoo YAML data into various formats
"""
import argparse
import os.path
import glob

import yaml


def find_db():
    """

    Assume that ref/ directory is at same level as this file (panbib.py).
    """
    ref_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ref')
    return glob.glob(os.path.join(ref_path, '*.yaml'))

def flatten_year_files(paths):
    entries = dict()
    for path in paths:
        try:
            int(os.path.basename(path).split('.')[0])
        except ValueError:
            continue
        with open(path) as fp:
            incoming = yaml.load(fp)
        entries.update(incoming)
    return entries


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gr1py')
    parser.add_argument('-t', '--type', metavar='TYPE', action='store',
                        help='output format; support formats: bibtex')
    args = parser.parse_args()

    db_files = find_db()
    entries = flatten_year_files(db_files)
