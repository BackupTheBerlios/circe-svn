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
from window_channel import window_channel

class panel_windowarea(wx.Panel):
    def __init__(self,parent,panelID):
        wx.Panel.__init__(self,parent,panelID)
        self.windowList = []
        self.func_addwindow = None
        self.func_delwindow = None
        self.func_showwindow = None
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
        #self.testWindow = wx.TextCtrl(self,-1,"Test Window Area. (Window 1)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow2 = wx.TextCtrl(self,-1,"Test Window Area. (Window 2)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow = window_channel(self,-1)
        #self.testWindow2 = window_channel(self,-1)
        #self.AddWindow(self.testWindow)
        #self.AddWindow(self.testWindow2)
        #self.ShowWindow(self.testWindow)
        #self.ShowWindow(self.testWindow2)
    
    def AddWindow(self,window,caption):
        if(window in self.windowList):
            raise "Window %s already exists" % window
        else:
            self.windowList.append(window)
            window.Show(False)
            if(self.func_addwindow is not None):
                self.func_addwindow(window,caption)
    
    def RemoveWindow(self,window):
        if(window in self.windowList):
            self.sizer_Top.Remove(window)
            self.windowList[self.windowList.index(window)] = None
            if(self.func_delwindow is not None):
                self.func_delwindow(window)
        else:
            raise "Window: %s does not exist in windows list" % window
    
    def ShowWindow(self,window):
        if(window in self.windowList):
            for winToHide in self.windowList:
                winToHide.Show(False)
                self.sizer_Top.Remove(winToHide)
            window.Show(True)
            self.sizer_Top.Add(window,1,wx.EXPAND)
            self.sizer_Top.Layout()
            if(self.func_showwindow is not None):
                self.func_showwindow(window)
        else:
            raise "Window: %s does not exist in windows list" % window
    
    def CreateControls(self):
        pass
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        pass

    def BindAdd(self,func):
        self.func_addwindow = func

    def BindDel(self,func):
        self.func_delwindow = func

    def BindShow(self,func):
        self.func_showwindow = func
