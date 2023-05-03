# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

from flightplandb import __version__

sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "FlightplanDB-py"
copyright = "2022, PH-KDX"
author = "PH-KDX"

# The full version, including alpha/beta/rc tags
release = __version__
# readthedocs.io insists on the version field being filled for epub builds
version = release


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinx.ext.autodoc",  # HTML generation from docstrings
    "sphinx.ext.napoleon",  # Read NumPy style docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary

autodoc_member_order = "bysource"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "../../artwork/png/120x120.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "../../artwork/ico/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

smartquotes = False

pygments_style = "sphinx"


def setup(app):
    app.add_css_file("css/colourscheme.css")
