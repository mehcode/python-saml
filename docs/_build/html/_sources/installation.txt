Installation
============

Supported platforms
-------------------
 - Python 2.7
 - Python 3.3
 - Python 3.4

Dependencies
------------

In order to sign and verify signatures, `libxml2` and `libxmlsec` are required.

Linux
::
    apt-get install libxml2-dev libxmlsec1-dev

Mac
::
    brew install libxml2 libxmlsec1


Installing an official release
------------------------------

The most recent release is available from PyPI
::
    pip install saml

Installing the development version
----------------------------------

1. Clone the **python-saml** repository
::
    git clone git://github.com/mehcode/python-saml.git

2. Change into the project directory
::
    cd python-saml

3. Install the project and all its dependencies using `pip`
::
    pip install .
