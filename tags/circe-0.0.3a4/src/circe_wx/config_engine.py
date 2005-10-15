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

class Config(object):
    def __init__(self, configsection="Circe", configfile="~/.circe/config"):
        self.config = ConfigParser.ConfigParser()
        self.configfile = os.path.expanduser(configfile)
        self.config.readfp(open(self.configfile, "r"))
        self.section = configsection

    def __getitem__(self, k):
        result = self.__dict__.get("initialized", False)
        if not result:
            if self.__dict__.has_key(k):
                return self.__dict__[k]
            
        if k[0] == '_':
            raise KeyError, k
        try:
            return self.config.get(self.section, k)
        except ConfigParser.NoSectionError:
            raise KeyError, k
    def __setitem__(self, k, v):
        if k[0] == '_' or k == '__dict__':
            raise KeyError, k
        if 'config' in k or 'section' in k:
            return
        self.config.set(self.section, k, v)
        self.__dict__[k] = v
        self.config.write(open(self.configfile, "w"))

    def __delitem__(self, k):
        self.config.remove_option(self.section, k)
        self.config.write(open(self.configfile, "w"))

    def __getattr__(self, k):
        try: return object.__getattr__(self, k)
        except AttributeError: pass
        try:
            return getattr(circe_config, k)
        except AttributeError: pass
        try: return self[k]
        except KeyError: pass
        return getattr(self.config, k)
    def getboolean(self, k):
        return self.config.getboolean(self.section, k)
