#!/bin/env python
"""panbib - map tlzoo YAML data into various formats
"""
from __future__ import print_function
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

def print_bibtex(entries):
    monthtext = ['January', 'February', 'March', 'April', 'May',
                 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']
    for key, entry in entries.items():
        if entry['type'] == 'conference paper':
            print('@inproceedings{{{KEY},\n'
                  '  title = {{{TITLE}}},\n'
                  '  author = {{{AUTHORS}}},\n'
                  '  year = {{{YEAR}}},\n'
                  '  month = {{{MONTH}}},\n'
                  '  booktitle = {{{BOOKTITLE}}},\n'
                  '}}'.format(
                      KEY=key,
                      TITLE=entry['title'],
                      AUTHORS=' AND '.join(entry['authors']),
                      YEAR=entry['year'],
                      MONTH=monthtext[entry['month']-1],
                      BOOKTITLE=entry['booktitle']
                  ))
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gr1py')
    parser.add_argument('-t', '--type', metavar='TYPE', action='store',
                        dest='out_format',
                        help='output format; support formats: bibtex')
    args = parser.parse_args()

    db_files = find_db()
    entries = flatten_year_files(db_files)

    target_format = args.out_format.lower()
    if target_format == 'bibtex':
        print_bibtex(entries)
    else:
        pass
