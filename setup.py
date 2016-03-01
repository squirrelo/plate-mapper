#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2013--, platemapper development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
from setuptools import find_packages, setup
from distutils.command.build_py import build_py
from glob import glob

__version__ = '0.1.0'

classes = """
    Development Status :: 1 - Planning
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python
    Programming Language :: Python :: 3.5
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

long_description = 'Knight lab source tracking project'

setup(name='plate-mapper',
      cmdclass={'build_py': build_py},
      version=__version__,
      license='BSD',
      description='plate-mapper: simplified sample and run tracking',
      long_description=long_description,
      author='Joshua Shorenstein',
      author_email='jshorens@gmail.com',
      maintainer='Joshua Shorenstein',
      maintainer_email='jshorens@gmail.com',
      url='https://github.com/squirrelo/plate-tracker',
      packages=find_packages(),
      package_data={
          'platemap': ['db/*.sql']
      },
      scripts=glob('scripts/*'),
      extras_require={'test': ['nose >= 0.10.1', 'flake8', 'mock',
                               'requests_toolbelt']},
      install_requires=['tornado', 'psycopg2', 'passlib', 'bcrypt', 'wtforms',
                        'click'],
      classifiers=classifiers)
