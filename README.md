The Specification Language Zoo
------------------------------

The site is deployed at <https://tlzoo.party>

The ambition of this repository is to concisely document all specification
languages and their relationships as presented in published papers. It aspires
to be a comprehensive listing of specification languages that have been
described in the literature, along with salient results and properties, e.g.,
computational complexity and expressiveness relative to other specification
languages. Each listing must have the first (known) paper that introduced the
specification language, and it must have citations for each property, where
readers can find proofs etc.

The scope for inclusion is potential applicability in robotics and, in general,
hybrid systems. Note that specification languages developed for concurrent
systems and other settings classically treated in the formal verification
literature are still in scope.


Organization
------------

There are two main parts to this repository: the collection of [YAML](
https://yaml.org/) files that stores all data about specification languages, and
scripts for deploying a website that hosts search-able access to these data.
Building the site is described below. Note that contributing new entries does
not require capability to build and deploy the website.


Participating
-------------

To report errors, to propose changes to existing entries, or to suggest the
addition of new material, please use the issue tracker at
<https://github.com/fmrchallenge/tlzoo/issues>.

More details about contributing material are in [contributing](CONTRIBUTING.md).


Building the website
--------------------

Python is required. Everything in known to work on GNU/Linux. Testers and
contributors for other platforms are welcome! The primary dependencies are
[PyYAML](https://pyyaml.org/wiki/PyYAML), [MkDocs](https://www.mkdocs.org/), and
the [`mdx_math` extension for Python-Markdown](
https://github.com/mitya57/python-markdown-math).
To install them, try

    pip install pyyaml mkdocs python-markdown-math

Now, to build the website content,

    ./build.sh

The output will be placed under the directory site/site/. It can be served using
any static web hosting service. During development, a locally hosted view can be
obtained by running `./build.sh serve` and directing your web browser to
http://127.0.0.1:8000


License
-------

This work is released under the Creative Commons Attribution 4.0 International
License. To get a copy of this license, visit
<https://creativecommons.org/licenses/by/4.0/>
or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
