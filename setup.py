# -*- coding: utf-8 -*-
"""Template setup.py Read more on
https://docs.python.org/3.7/distutils/setupscript.html."""

import sys

from setuptools import setup

sys.path.append("./oxapi/")

from pathlib import Path

long_description = Path("README.md").read_text()

NAME = "oxapi"
VERSION = "1.1.2"
DESCRIPTION = "The Python library for querying the OxAPI"
AUTHOR = "Oxolo GmbH"
AUTHOR_EMAIL = "support@oxapi.ai"
PACKAGES = ["oxapi", "oxapi.nlp", "oxapi.abstract"]
INSTALL_REQUIRES = [
    "grequests>=0.6.0",
    "numpy>=1.17",
    "pandas>=1.3",
    "requests>=2.27",
    "urllib3>=1.26.5",
    "jinja2>=2.11.3",
    "hypothesis>=6.54.3",
    "jedi>=0.10",
]

PROJECT_URLS = {"Source Code": "https://github.com/Oxolo/oxapi-python"}

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
    project_urls=PROJECT_URLS,
)
