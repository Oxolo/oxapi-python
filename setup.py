# -*- coding: utf-8 -*-
"""Template setup.py Read more on
https://docs.python.org/3.7/distutils/setupscript.html."""

import sys

from setuptools import setup

sys.path.append("./oxapi/")

from config import version

NAME = "oxapi"
VERSION = version
DESCRIPTION = ""
AUTHOR = ""
AUTHOR_EMAIL = ""
PACKAGES = ["oxapi", "oxapi.nlp", "oxapi.abstract"]
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
