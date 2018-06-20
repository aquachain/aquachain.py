#!/usr/bin/env python3
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    install_requires = requirements,
    name='aquachain.py',
    url='https://github.com/aquachain/aquachain.py',
    packages = ['aquachain'],
    version='0.0.1',
    description='Aquachain for Python 3.6.5',
    author='aerth',
    author_email='aerth@riseup.net',
    license = 'GPL',
    test_suite='aquachain.tests',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License (GPL)',
	],
)
