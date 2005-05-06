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

class panel_tree(wx.Panel):
    def __init__(self,parent,panelID,treesize=-1):
        self.treesize = (treesize,-1)
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.treesize)
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        self.testArea = wx.TextCtrl(self,-1,"Test Tree Area",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.testArea,1,wx.EXPAND)
