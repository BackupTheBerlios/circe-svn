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
from panel_window import panel_window
import servermanager

ID_TXT_EDIT = wx.NewId()

class window_status(panel_window):
    def __init__(self,parent,server,id=-1):
        self.server = server
        server.SetStatusWindow(self)
        self.caption = self.MakeCaption()
        panel_window.__init__(self,parent,id,self.caption)
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()

    def MakeCaption(self):
        if self.server.host != None:
            c = self.server.host
        else:
            c = "Status"
        return c
    
    def CreateControls(self):
        self.txtBuffer = wx.TextCtrl(self,-1,"Server: %s\n" % self.server.host,wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.txtEdit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)
        #self.txtEdit.Bind(wx.EVT_CHAR, self.txtEdit_EvtChar)
        wx.EVT_CHAR(self.txtEdit,self.txtEdit_EvtChar)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.txtBuffer,1,wx.EXPAND)
        self.sizer_Top.Add(self.txtEdit,0,wx.EXPAND)

    def txtEdit_EvtChar(self, event):
        key = event.GetKeyCode()
        if(key == 13):
            # Enter pressed
            servermanager.TextCommand(self.server,self.txtEdit.GetValue())
            self.txtEdit.SetValue("")
        else:
            event.Skip()

    def ServerEvent(self, event):
        self.txtBuffer.AppendText("%s\n" % event)
