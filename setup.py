#!/usr/bin/env python3
from setuptools import setup
version = '0.0.4'
setup(
    install_requires = ['base58', 'mnemonic', 'web3', 'ethereum'],
    name='aquachain.py',
    url='https://github.com/aquachain/aquachain.py',
    packages = ['aquachain'],
    version=version,
    description='Aquachain for Python 3.6.5',
    long_description='Aquachain for Python 3.6.5 -- See https://github.com/aquachain/aquachain.py or https://aquachain.github.io for more information.',
    author='Aquachain Authors',
    author_email='aquachain@riseup.net',
    license = 'GPL',
    test_suite='aquachain.tests',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License (GPL)',
	],
)
