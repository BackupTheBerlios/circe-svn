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

currpath = os.path.join(os.getcwd(), __file__)
currpath = os.path.abspath(os.path.join(currpath, '../..'))
sys.path.insert(0, currpath)

config_dir = os.path.join(os.path.expanduser('~'), '.circe')
if not os.path.exists(config_dir):
    os.mkdir(config_dir)

sys.path.insert(0, config_dir)

config_file = os.path.join(config_dir, 'config.py')
if not os.path.exists(config_file):
    import circe_config
    sys.modules["config"] = circe_config

from circe_wx.frame_main import frame_main

def handle_exc(message):
    print message
    traceback.print_exc()

class CirceApp(wx.App): 
    def OnInit(self):
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
