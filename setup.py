#!/usr/bin/env python
from setuptools import setup, find_packages
import codecs
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="flightplandb",
    version=get_version("src/flightplandb/__init__.py"),
    author="PH-KDX",
    url="https://github.com/PH-KDX/flightplandb-py/",
    project_urls={
        "Documentation": "https://flightplandb-py.readthedocs.io/",
        "Issue tracker": "https://github.com/PH-KDX/flightplandb-py/issues",
    },
    description="Python wrapper for the Flight Plan Database API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "requests==2.26.0",
        "python-dateutil==2.8.2"
    ],
    extras_require={
        "dev": [
            "Sphinx==4.5.0",
            "sphinx-rtd-theme==1.0.0"
        ],
        "test": [
            "pytest~=6.2.5",
            "pytest-mock~=3.6.1",
            "pytest_socket~=0.4.1"
        ]
    },
    python_requires='>=3.7.0',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Games/Entertainment :: Simulation"
    ]
)
