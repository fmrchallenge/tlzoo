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

def generate_bibtex(entry, key=None):
    monthtext = ['January', 'February', 'March', 'April', 'May',
                 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']
    if entry['type'] == 'conference paper':
        return ('@inproceedings{{{KEY},\n'
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
    elif entry['type'] == 'article':
        return ('@article{{{KEY},\n'
                '  title = {{{TITLE}}},\n'
                '  author = {{{AUTHORS}}},\n'
                '  year = {{{YEAR}}},\n'
                '  journal = {{{JOURNAL}}},\n'
                '}}'.format(
                    KEY=key,
                    TITLE=entry['title'],
                    AUTHORS=' AND '.join(entry['authors']),
                    YEAR=entry['year'],
                    JOURNAL=entry['journal']
                ))

def print_bibtex_list(entries):
    for key, entry in entries.items():
        print(generate_bibtex(entry, key=key))
        print()  # Blank line

def generate_tlzoo_tree(entries):
    """

    Output files are placed under the directory site/docs/
    """
    title_mapping = list(entries.keys())
    title_mapping.sort(key=(lambda x: entries[x]['title']))
    with open(os.path.join('site', 'mkdocs.yml'), 'w') as fp:
        with open(os.path.join('site', 'mkdocs.yml.prefix')) as fp_prefix:
            fp.write(fp_prefix.read())
        fp.write('- papers:\n')
        for key in title_mapping:
            fp.write('  - "{TITLE}": papers/{KEY}.md\n'.format(
                TITLE=entries[key]['title'],
                KEY=key
            ))

    docs_dir = os.path.join('site', 'docs')
    papers_dir = os.path.join(docs_dir, 'papers')
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    if not os.path.exists(papers_dir):
        os.mkdir(papers_dir)
    for key, entry in entries.items():
        with open(os.path.join(papers_dir, key+'.md'), 'w') as fp:
            if entry['type'] == 'conference paper':
                venue = entry['booktitle']
            elif entry['type'] == 'article':
                venue = entry['journal']
            else:
                venue = '(UNKNOWN)'
            fp.write('''## {TITLE}

**authors:** {AUTHORS}

**venue:** {VENUE}

**date:** {DATE}
'''.format(TITLE=entry['title'],
           AUTHORS=', '.join(entry['authors']),
           VENUE=venue,
           DATE=entry['year'])
                     )

            fp.write('### keywords\n\n')
            if ('keywords' in entry) and len(entry['keywords']) > 0:
                fp.write(', '.join(entry['keywords']))
            else:
                fp.write('(nil)')
            fp.write('\n\n')

            fp.write('### URL\n\n')
            if ('url' in entry) and len(entry['url']) > 0:
                fp.write('\n'.join(['* <'+url+'>' for url in entry['url']]))
            else:
                fp.write('(nil)')
            fp.write('\n\n')

            fp.write('### BibTeX\n<pre>\n')
            fp.write(generate_bibtex(entry))
            fp.write('</pre>\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='panbib')
    parser.add_argument('-t', '--type', metavar='TYPE', action='store',
                        dest='out_format', default='bibtex',
                        help='output format; support formats: bibtex, tlzoo')
    args = parser.parse_args()

    db_files = find_db()
    entries = flatten_year_files(db_files)

    target_format = args.out_format.lower()
    if target_format == 'bibtex':
        print_bibtex_list(entries)
    elif target_format == 'tlzoo':
        generate_tlzoo_tree(entries)
    else:
        pass
