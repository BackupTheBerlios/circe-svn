# Circe
# Copyright (C) 2004 The Circe development team

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

import wx
import traceback
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

if(__name__ == "__main__"):
    circe = CirceApp(0)
    circe.MainLoop()