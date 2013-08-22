# -*- coding: utf-8 -*-
import sys
from os import path

# Get the base path.
base = path.join(path.dirname(__file__), '..')

# Append the source directory to PATH.
sys.path.append(path.join(base, 'src'))
