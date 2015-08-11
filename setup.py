#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup the vetodef package
"""

from __future__ import print_function

import sys
if sys.version < '2.6':
    raise ImportError("Python versions older than 2.6 are not supported.")

import glob
import hashlib
import os.path
import subprocess

try:
    import setuptools
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
finally:
    from setuptools import (setup, find_packages)
    from setuptools.command import (build_py, egg_info)

from distutils import log
from distutils.dist import Distribution
from distutils.cmd import Command
from distutils.command.clean import (clean, log, remove_tree)

# test for OrderedDict
extra_install_requires = []
try:
    import argparse
except ImportError:
    extra_install_requires.append('argparse')

# set basic metadata
PACKAGENAME = 'ligovirgo-vetodef'
AUTHOR = 'Duncan Macleod'
AUTHOR_EMAIL = 'duncan.macleod@ligo.org'
LICENSE = 'GPLv3'

# -- process dependencies -----------------------------------------------------

# XXX: this can be removed as soon as a stable release of glue can
#      handle pip/--user
try:
    from glue import git_version
except ImportError as e:
    e.args = ("LIGO-Virgo VetoDef requires the GLUE package, "
              "which isn\'t available from PyPI.\nPlease visit\n"
              "https://www.lsc-group.phys.uwm.edu/daswg/projects/glue.html\n"
              "to download and install it manually.",)
    raise


# -- find files ---------------------------------------------------------------

# Use the find_packages tool to locate all packages and modules
packagenames = find_packages()

# glob for all scripts
if os.path.isdir('bin'):
    scripts = glob.glob(os.path.join('bin', '*'))
else:
    scripts = []

# -- run setup ----------------------------------------------------------------

setup(name=PACKAGENAME,
      provides=[PACKAGENAME.split('-')[-1]],
      version=None,
      description=None,
      long_description=None,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=packagenames,
      scripts=scripts,
      setup_requires=['setuptools'],
      requires=[
          'argparse',
          'glue',
      ],
      install_requires=[
      ] + extra_install_requires,
      dependency_links=[
          'https://www.lsc-group.phys.uwm.edu/daswg/download/'
          'software/source/glue-1.48.tar.gz#egg=glue-1.48',
      ],
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
)
