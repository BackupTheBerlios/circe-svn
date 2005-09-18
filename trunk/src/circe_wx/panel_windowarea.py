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
from window_channel import WindowChannel
import servermanager

class PanelWindowarea(wx.Panel):
    def __init__(self,parent,panelID):
        wx.Panel.__init__(self,parent,panelID)
        self.window_list = []
        self.func_addwindow = None
        self.func_delwindow = None
        self.func_showwindow = None
        self.func_setcaption = None
        self.create_controls()
        self.create_sizers()
        self.add_controls()
        
        #self.testWindow = wx.TextCtrl(self,-1,"Test Window Area. (Window 1)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow2 = wx.TextCtrl(self,-1,"Test Window Area. (Window 2)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow = WindowChannel(self,-1)
        #self.testWindow2 = WindowChannel(self,-1)
        #self.add_window(self.testWindow)
        #self.add_window(self.testWindow2)
        #self.show_window(self.testWindow)
        #self.show_window(self.testWindow2)
    
    def new_server(self):
        s = servermanager.add_server(self)
        self.show_window(s.statuswindow.section_id,s.statuswindow)

    def add_server(self):
        """Create a new window status to make a new connection."""
        s = servermanager.add_server(self)
        return s

    def add_window(self,section,window):
        if window in self.window_list:
            raise "Window %s already exists" % window
        else:
            self.window_list.append(window)
            window.Show(False)
            if self.func_addwindow != None:
                caption = window.get_caption()
                self.func_addwindow(section,window,caption)
    
    def remove_window(self,section,window):
        if window in self.window_list:
            self.sizer_top.Remove(window)
            index = self.window_list.index(window)
            del self.window_list[index]
            if self.func_delwindow is not None:
                self.func_delwindow(section,window)
                if len(self.window_list) > 0:
                    self.show_window(self.window_list[index-1].server, self.window_list[index-1])
        else:
            raise "Window: %s does not exist in windows list" % window
    
    def show_window(self,section,window,ignoreEvent=False):
        if window in self.window_list:
            for winToHide in self.window_list:
                winToHide.Show(False)
                self.sizer_top.Remove(winToHide)
            window.Show(True)
            window.evt_focus()
            self.sizer_top.Add(window,1,wx.EXPAND)
            self.sizer_top.Layout()
            if not ignoreEvent:
                if self.func_showwindow is not None:
                    self.func_showwindow(section,window)
        else:
            raise "Window: %s does not exist in windows list" % window

    def set_caption(self,section,window,caption):
        if window in self.window_list:
            if self.func_setcaption is not None:
                    self.func_setcaption(section,window,caption)
    
    def create_controls(self):
        pass
    
    def create_sizers(self):
        self.sizer_top = wx.BoxSizer()
        self.SetSizer(self.sizer_top)
    
    def add_controls(self):
        pass

    def bind_add(self,func):
        self.func_addwindow = func

    def bind_del(self,func):
        self.func_delwindow = func

    def bind_show(self,func):
        self.func_showwindow = func

    def bind_set_caption(self,func):
        self.func_setcaption = func
