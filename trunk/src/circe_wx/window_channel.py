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
import lorem
#import commandparser
from panel_window import panel_window
from window_server import window_server

ID_TXT_EDIT = wx.NewId()
ID_LST_USERS = wx.NewId()

class window_channel(window_server):
    def __init__(self,windowarea,id,server):
        window_server.__init__(self,windowarea,id,server,"Channel")
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        self.txtBuffer = wx.TextCtrl(self,-1,"Channel: %s\n\n%s" % (self.caption,lorem.text),wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.txtEdit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)
        self.lstUsers = wx.ListCtrl(self,ID_LST_USERS,wx.DefaultPosition,wx.DefaultSize)
        wx.EVT_CHAR(self.txtEdit,self.txtEdit_EvtChar)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_BufferAndUsers = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_BufferAndUsers.Add(self.txtBuffer,1,wx.EXPAND)
        self.sizer_BufferAndUsers.Add(self.lstUsers,0,wx.EXPAND)
        self.sizer_Top.Add(self.sizer_BufferAndUsers,1,wx.EXPAND)
        self.sizer_Top.Add(self.txtEdit,0,wx.EXPAND)

    def txtEdit_EvtChar(self, event):
        key = event.GetKeyCode()
        if(key == 13):
            # Enter pressed
            #self.TextCommand(self.txtEdit.GetValue())
            #commandparser.TextCommand(self.server,self.windowarea,self.txtEdit.GetValue())
            self.txtEdit.SetValue("")
        else:
            event.Skip()
