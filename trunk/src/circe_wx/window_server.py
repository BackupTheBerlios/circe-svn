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

import wx
from panel_window import panel_window

class window_server(panel_window):
    def __init__(self,windowarea,server,caption=None):
        self.windowarea = windowarea
        self.server = server
        panel_window.__init__(self,windowarea,caption)

        self.txtBuffer = wx.TextCtrl(self,-1,"",wx.DefaultPosition,
                wx.DefaultSize,wx.TE_MULTILINE)
        self.txtBuffer.SetEditable(False)
        f = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Monospace")
        self.txtBuffer.SetDefaultStyle(wx.TextAttr("BLACK", wx.NullColour, f))

    def getWindowarea(self):
        return self.windowarea

    def getServer(self):
        return self.server

    def ServerEvent(self, event):
        """Displays an event in the text buffer."""
        self.txtBuffer.AppendText(event+"\n")

    def evt_caption(self):
        self.windowarea.SetCaption(self.server,self,self.caption)
