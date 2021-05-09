#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="flightplandb",
    version="0.3.0",
    author="PH-KDX",
    author_email="smtp.python.email.sender@gmail.com",
    url="https://github.com/PH-KDX/flightplandb-py/",
    packages=find_packages(),
    install_requires=[
        "requests==2.25.1",
        "python-dateutil==2.8.1"
    ],
    extras_require={
        "dev": [
            "Sphinx==4.0.0",
            "sphinx-rtd-theme==0.5.2"
        ]
    }
)
