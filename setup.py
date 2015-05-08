#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def requires(*f):
    return [
        r for r in (
            strip_comments(l) for l in open(
                os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]


with open('README.rst') as fh:
    long_description = fh.read()

    
setup(
    name='ptb',
    install_requires = requires('requirements.txt'),
    packages=find_packages(),
    version='0.0.2',
    description='ptb - Python TraceBack for Humans',
    long_description=long_description,
    keywords = 'traceback debugging',
    author='Anand Reddy Pandikunta (@chillaranand)',
    author_email='anand21nanda@gmail.com',
    maintainer='Anand Reddy Pandikunta',
    maintainer_email='anand21nanda@gmail.com',
    url='https://github.com/chillaranand/ptb',
    data_files=[],
    classifiers=[
          'Development Status :: 1 - Planning',
          
          'Operating System :: POSIX',
          
          'Programming Language :: Python', 
          'Programming Language :: Python :: 2.7', 
          'Programming Language :: Python :: 3', 
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          
          'Intended Audience :: Developers',

          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities'
          ],
)


