# -*- coding: utf-8 -*-
"""Template setup.py Read more on
https://docs.python.org/3.7/distutils/setupscript.html."""

from setuptools import setup

NAME = "oxapi-python"
VERSION = "0.0.2"
DESCRIPTION = "The OxAPI Python library provides simplified access to the OxAPI from applications written in the Python language."
AUTHOR = ""
AUTHOR_EMAIL = ""
PACKAGES = ["oxapi"]
INSTALL_REQUIRES = ["grequests>=0.6.0", "numpy>=1.17", "pandas>=1.3"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
)
