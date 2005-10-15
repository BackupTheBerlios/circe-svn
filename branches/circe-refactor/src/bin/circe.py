#!/usr/bin/env python

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

__revision__ = "$Id: circe.py 123 2005-05-06 18:03:00Z anjel $"

import wx
import traceback
import sys, os
import platform
# Importing section

currpath = os.path.join(os.getcwd(), __file__)
currpath = os.path.abspath(os.path.join(currpath, '../..'))
sys.path.insert(0, currpath)

config_dir = os.path.join(os.path.expanduser('~'), '.circe')
if not os.path.exists(config_dir):
    os.mkdir(config_dir)

if platform.system() != "Windows":
    config_file = os.path.join(config_dir, 'config')
else:
    config_file = os.path.join(config_dir, 'config.ini')

import circe_wx.config_engine as config_engine
config = config_engine.Config(configfile=config_file)

from circe_wx.frame_main import frame_main, CheckVersion

def handle_exc(message):
    print message
    traceback.print_exc()

class CirceApp(wx.App):
    def OnInit(self):
        WXVER = "2.6"
        version = wx.VERSION_STRING.split('.')
        major, patchlevel = version[0], version[1]
        NOW = '.'.join([major, patchlevel])
        if NOW != WXVER:
            result = wx.MessageBox(
              "This application is known to be compatible with\n"
              "wxPython version(s) %s, but you have %s installed.\n"
              "\nWould you like to continue?" % (WXVER, NOW),
              "wxPython Version Warning",
              wx.YES_NO)
            if result == wx.NO:
                return False # Exit
        try:
            if config.getboolean("check_version"):
                cv = CheckVersion("frm_bin")
        except KeyError: pass
        try:
            self.mainFrame = frame_main()
            self.mainFrame.Show(True)
            self.SetTopWindow(self.mainFrame)
        except:
            handle_exc("Error on application init:")
        return True

if __name__ == "__main__":
    circe = CirceApp(0)
    circe.MainLoop()
