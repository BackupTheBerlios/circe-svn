#!/usr/bin/python

import os, sys

rn = raw_input("Name of release: ")
vn = raw_input("Version: ")

os.system("svn export . ~/%s-%s" % (rn, vn))
os.system("cd")
os.system("tar -cf %s-%s %s-%s.tar.gz" % (rn, vn, rn, vn))
