#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="flightplandb",
    version="0.3.1",
    author="PH-KDX",
    author_email="smtp.python.email.sender@gmail.com",
    url="https://github.com/PH-KDX/flightplandb-py/",
    project_urls={
        "Documentation": "https://flightplandb-py.readthedocs.io/",
        "Issue tracker": "https://github.com/PH-KDX/flightplandb-py/issues",
    },
    description="Python wrapper for the Flight Plan Database API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests==2.25.1",
        "python-dateutil==2.8.1"
    ],
    extras_require={
        "dev": [
            "Sphinx==4.0.0",
            "sphinx-rtd-theme==0.5.2"
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
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Games/Entertainment :: Simulation"
    ]
)
