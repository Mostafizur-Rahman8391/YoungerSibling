# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath('../..'))

# Project information
project = 'YoungerSibling'
copyright = '2024, Mostafizur Rahman'
author = 'Mostafizur Rahman'
release = '1.2'

# General configuration
extensions = [
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.viewcode',  # Add links to source code
]
templates_path = ['_templates']
exclude_patterns = []

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
