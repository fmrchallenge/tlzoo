#!/bin/sh -e

./panbib.py -t tlzoo
cp -f README.md site/docs/index.md
cp -f CONTRIBUTING.md site/docs/
cd site && mkdocs build

if [ "$1" == "serve" ]; then
    mkdocs serve
fi
