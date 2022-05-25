# -*- coding: utf-8 -*-
"""Template setup.py Read more on
https://docs.python.org/3.7/distutils/setupscript.html."""

from setuptools import setup

NAME = "pptemplate"
VERSION = "1.0.3"
DESCRIPTION = "This is a template project for python. You can change it on will to match your requirements"
AUTHOR = "Naser Derakhshan"
AUTHOR_EMAIL = "n.derakhshan@oxolo.com"
PACKAGES = ["mypackage"]
INSTALL_REQUIRES = ["ConfigArgParse==1.5.3", "numpy==1.22.3"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
)
