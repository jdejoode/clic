"""clic setup file."""

from __future__ import with_statement

import inspect
import os
import re

# Import Setuptools
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

from clic.setuptools.commands import develop, install

name_ = 'clic'
version_ = '0.1'
description_ = "CLiC Project"

# Inspect to find current path
setuppath = inspect.getfile(inspect.currentframe())
setupdir = os.path.dirname(setuppath)

# Requirements

# Description
with open(os.path.join(setupdir, 'README.rst'), 'r') as fh:
    long_description_ = fh.read()


setup(
    name = name_,
    version = version_,
    description = description_,
    long_description=long_description_,
    packages=['clic'],
    requires=['webob'],
    author = 'Catherine Smith',
    maintainer = 'John Harrison',
    maintainer_email = u'john.harrison@liv.ac.uk',
    license = "BSD",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
    ],
    cmdclass = {
        'develop': develop,
        'install': install
    },
)
