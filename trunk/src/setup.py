#!/usr/bin/python

from distutils.core import setup

setup(
    name="circe",
    version="0.0.3a5",
    url="http://circe.berlios.de",
    description="A GUI-based IRC Client written in Python",
    license="GPL",
    packages=['circelib', 'circe_wx'],
    scripts=['circe.py']
)
