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

def parse_db(paths):
    paper_entries = dict()
    spc_entries = dict()

    for path in paths:
        if os.path.basename(path) == 'def.yaml':
            with open(path) as fp:
                spc_entries = yaml.load(fp)
            continue
        try:
            int(os.path.basename(path).split('.')[0])
        except ValueError:
            continue
        with open(path) as fp:
            incoming = yaml.load(fp)
        paper_entries.update(incoming)
    return spc_entries, paper_entries

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

def generate_tlzoo_tree(spc_entries, paper_entries):
    """

    Output files are placed under the directory site/docs/
    """
    with open(os.path.join('site', 'mkdocs.yml'), 'w') as fp:
        with open(os.path.join('site', 'mkdocs.yml.prefix')) as fp_prefix:
            fp.write(fp_prefix.read())

        title_mapping = list(spc_entries.keys())
        title_mapping.sort(key=(lambda x: spc_entries[x]['name']))
        fp.write('- specification languages:\n')
        for key in title_mapping:
            fp.write('  - "{NAME}": spc/{KEY}.md\n'.format(
                NAME=spc_entries[key]['name'],
                KEY=key
            ))

        title_mapping = list(paper_entries.keys())
        title_mapping.sort(key=(lambda x: paper_entries[x]['title']))
        fp.write('- papers:\n')
        for key in title_mapping:
            fp.write('  - "{TITLE}": papers/{KEY}.md\n'.format(
                TITLE=paper_entries[key]['title'],
                KEY=key
            ))

    docs_dir = os.path.join('site', 'docs')
    spc_dir = os.path.join(docs_dir, 'spc')
    papers_dir = os.path.join(docs_dir, 'papers')
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    if not os.path.exists(spc_dir):
        os.mkdir(spc_dir)
    if not os.path.exists(papers_dir):
        os.mkdir(papers_dir)

    for key, entry in spc_entries.items():
        with open(os.path.join(spc_dir, key+'.md'), 'w') as fp:
            fp.write('''## {NAME}
'''.format(NAME=entry['name'])
                     )

    for key, entry in paper_entries.items():
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
    spc_entries, paper_entries = parse_db(db_files)

    target_format = args.out_format.lower()
    if target_format == 'bibtex':
        print_bibtex_list(paper_entries)
    elif target_format == 'tlzoo':
        generate_tlzoo_tree(spc_entries, paper_entries)
    else:
        pass
