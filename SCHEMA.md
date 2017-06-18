Introduction
------------

The website is generated from a collection of [YAML](http://yaml.org/) files.
Each reference is placed in a file according to the year of its publication and
has a unique identifier associated with it.


Example
-------

```
d6a38902-18ae-4de1-bcfa-ce6af34a62f3:
  title: Example Paper
  authors: Ada
```


Details
-------

Each entry has a corresponding unique identifier. Currently we are using version
4 UUIDs as defined in [RFC 4122](https://tools.ietf.org/html/rfc4122.html) and
as implemented in the Python standard library module
[uuid](https://docs.python.org/3.5/library/uuid.html).
