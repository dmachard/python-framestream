#!/usr/bin/python

import setuptools

with open("./fstrm/__init__.py", "r") as fh:
    for line in fh.read().splitlines():
        if line.startswith('__version__'):
            PKG_VERSION = line.split('"')[1]
            
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('framestreams fstrm encoder decoder')

setuptools.setup(
    name="fstrm",
    version=PKG_VERSION,
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Frame Streams implementation in Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/python-framestream",
    packages=['fstrm'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[]
)
