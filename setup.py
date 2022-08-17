# -*- coding: utf-8 -*-
"""Template setup.py Read more on
https://docs.python.org/3.7/distutils/setupscript.html."""

import sys

from setuptools import setup

sys.path.append("./oxapi/")

from pathlib import Path

long_description = Path("README.md").read_text()

NAME = "oxapi"
VERSION = "1.0.0"
DESCRIPTION = ""
AUTHOR = ""
AUTHOR_EMAIL = ""
PACKAGES = ["oxapi", "oxapi.nlp", "oxapi.abstract"]
INSTALL_REQUIRES = [
    "grequests>=0.6.0",
    "numpy>=1.17",
    "pandas>=1.3",
    "requests>=2.27",
    "urllib3>=1.26.5",
    "jinja2==2.11.3",
    "loguru==0.6.0",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
