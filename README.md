# python-saml
[![Build Status](https://travis-ci.org/mehcode/python-saml.png?branch=master)](https://travis-ci.org/mehcode/python-saml)
[![Coverage Status](https://coveralls.io/repos/mehcode/python-saml/badge.png?branch=master)](https://coveralls.io/r/mehcode/python-saml?branch=master)
[![PyPi Version](https://pypip.in/v/saml/badge.png)](https://pypi.python.org/pypi/saml)
![PyPi Downloads](https://pypip.in/d/saml/badge.png)
> A python interface to produce and consume Security Asserion Markup Language v2.0 (SAML2) messages.

## Features

##### Python 2.7.x, 3.3.x, 3.4.x support

python-saml supports both python 2.7.x+ and 3.3.x+.

##### SAML conformance

python-saml conforms to the latest [SAML][] (v2.0) standards.

[SAML]: https://www.oasis-open.org/standards#samlv2.0

##### Environment agnostic

python-saml may be used to produce and consume SAML messages regardless of the environment (terminal, WSGI, django) used to call it.

## Usage

###

Check the [test suite](https://github.com/mehcode/python-saml/blob/master/tests/saml/test_schema.py#L33) for additional examples on using the library.

## Install

### Automated

1. **saml** can be installed through `easy_install` or `pip`.

   ```sh
   pip install saml
   ```

### Manual

1. Clone the **saml** repository to your local computer.

   ```sh
   git clone git://github.com/mehcode/python-saml.git
   ```

2. Change into the **saml** root directory.

   ```sh
   cd /path/to/saml
   ```

3. Install the project and all its dependencies using `pip`.

   ```sh
   pip install .
   ```

## Contributing

### Setting up your environment

1. Follow steps 1 and 2 of the [manual installation instructions][].

[manual installation instructions]: #manual

2. Initialize a virtual environment to develop in.
   This is done so as to ensure every contributor is working with
   close-to-identicial versions of packages.

   ```sh
   mkvirtualenv saml
   ```

   The `mkvirtualenv` command is available from `virtualenvwrapper` which
   can be installed by following: http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation

3. Install **saml** in development mode with testing enabled.
   This will download all dependencies required for running the unit tests.

   ```sh
   pip install -e ".[test]"
   ```

### Running the test suite

1. [Set up your environment](#setting-up-your-environment).

2. Run the unit tests.

   ```sh
   py.test
   ```

## License
Unless otherwise noted, all files contained within this project are liensed under the MIT opensource license. See the included file LICENSE or visit [opensource.org][] for more information.

[opensource.org]: http://opensource.org/licenses/MIT
