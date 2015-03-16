Contributing
============

Setting up your environment
---------------------------

1. Fork the repository
2. Clone your fork
3. `Create a virtual environment <http://virtualenvwrapper.readthedocs.org/en/latest/install.html #basic-installation/>`_.
4. Install **python-saml** in development mode with testing enabled. This will download all dependencies required for running the unit tests.
::
    pip install -e ".[test]"
5. Make changes with tests and documentation
6. Open a pull request

Running the tests
-----------------

Tests are run with `py.test`.
::
    py.test --pep8 --flakes --cov saml

Testing documentation changes
-----------------------------

Documentation is handled with `Sphinx <http://sphinx-doc.org/>`_. Use the `make html` command in the `docs` directory to build an HTML preview of the documentation.
::
    cd docs
    make html
