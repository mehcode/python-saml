#! /usr/bin/env python
import os
from setuptools import setup, find_packages


setup(
    name='saml',
    version='0.2.1',
    description='A python interface to produce and consume Security Asserion Markup Language v2.0 (SAML2) messages.',
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    package_dir={'saml': 'src/saml'},
    packages=find_packages('src'),
    # TODO: Grep this from the appropriate requirements files.
    install_requires=('lxml',),
)
