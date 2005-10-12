#!/usr/bin/python

from distutils.core import setup

import os
from shutil import copyfile
import sys
import platform
    
def install_desktop_file():
    if platform.system() != "Linux":
        return

    try:
        ans = raw_input("Do you want to install a desktop icon that launches Circe? [y/N] ")
    except EOFError:
        ans = "n"
    if ans[0].lower() != "y":
        return

    to = "~/Desktop"
    to = os.path.expanduser(to)

    frompath = "./circe.desktop"

    try:
        copyfile(frompath, os.path.join(to, frompath))
    except OSError, e:
        pass
install_desktop_file()


setup(
    name="circe",
    version="0.0.3a4",
    url="http://circe.berlios.de",
    description="A GUI-based IRC Client written in Python",
    license="GPL",
    packages=['circelib', 'circe_wx'],
    scripts=['bin/circe.py']
)
if sys.argv[1] == "install":
    print "Circe sucessfully installed!"
