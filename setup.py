#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '0.1.0'


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()

setup(
    name='das-profiles',
    version=version,
    description="""Microservice to provide updated DAS Staff Directory Profile JSON data""",
    long_description=readme,
    author='Ryan Castner',
    author_email='rrcdis1@rit.edu',
    url='https://github.com/audiolion/das-profiles',
    packages=[
        'das-profiles',
    ],
    install_requires=[
        'apistar',
        'zappa'
    ],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='das-profiles, microservice, python, apistar',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
