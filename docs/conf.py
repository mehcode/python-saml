# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('../'))

from saml import __version__  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = ['.rst']
master_doc = 'index'

project = u'python-saml'
copyright = u'2015, Ryan Leckey'
author = u'Ryan Leckey'

version = __version__
release = version

exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'python-samldoc'
latex_elements = {}

latex_documents = [
  (master_doc, 'python-saml.tex', u'python-saml Documentation',
   u'Ryan Leckey', 'manual'),
]

man_pages = [
    (master_doc, 'python-saml', u'python-saml Documentation',
     [author], 1)
]

texinfo_documents = [
  (master_doc, 'python-saml', u'python-saml Documentation',
   author, 'python-saml', 'One line description of project.',
   'Miscellaneous'),
]
