#!/usr/bin/python
# Circe
# Copyright (C) 2004-2005 The Circe development team

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# Some imports...here we go!
import ConfigParser # we need some way to work with those damn INI config files ;)
import circe_config
import os

DEFAULTS = {
    "check_version": 1,
    "timestamp_show": 1,
    "time_format": "[%I:%M:%S]",
    "quitmsg": "Circe: http://circe.berlios.de/",
    "complete_suffix": ":"
}

class Config(object):
    def __init__(self, configsection="Circe", configfile="~/.circe/config"):
        self.config = ConfigParser.ConfigParser()
        self.configfile = os.path.expanduser(configfile)
        try:
            self.config.readfp(open(self.configfile, "r"))
        except IOError:
            print "Config file does not exist. TODO: Create proper config structure here!"
        self.section = configsection

    def __getitem__(self, k):
        try:
            return self.config.get(self.section, k)
        except ConfigParser.NoOptionError:
            try:
                v = DEFAULTS[k]
                self[k] = v
                return v
            except KeyError:
                raise KeyError, k
    def __setitem__(self, k, v):
        self.config.set(self.section, k, v)
        self.config.write(open(self.configfile, "w"))

    def __delitem__(self, k):
        try:
            self.config.remove_option(self.section, k)
            self.config.write(open(self.configfile, "w"))
        except ConfigParser.NoOptionError:
            raise KeyError,k
    def getboolean(self, k):
        try:
            return self.config.getboolean(self.section, k)
        except ConfigParser.NoOptionError:
            try:
                return DEFAULTS[k]
            except KeyError:
                return False
