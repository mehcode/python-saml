#! /usr/bin/env python
import os
from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read().strip()


setup(
    name='saml',
    version='0.2.0',
    description='A python interface to produce and consume Security Asserion Markup Language v2.0 (SAML2) messages.',
    long_description=read('README.md'),
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    package_dir={'saml': 'src/saml'},
    packages=find_packages('src'),
    # TODO: Grep this from the appropriate requirements files.
    install_requires=('lxml',),
)
