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
import circe_globals
import circe_config
import servermanager
from panel_switchbar import panel_switchbar
from panel_windowarea import panel_windowarea
from panel_tree import panel_tree
from window_channel import window_channel
from window_status import window_status

ID_MENU_FILE_ABOUT = wx.NewId()
ID_MENU_FILE_EXIT = 1002
ID_MENU_VIEW_SWITCHBAR = 1650
ID_MENU_VIEW_SWITCHBAR_ALEFT = 1651
ID_MENU_VIEW_SWITCHBAR_ARIGHT = 1652
ID_MENU_VIEW_SWITCHBAR_ATOP = 1653
ID_MENU_VIEW_SWITCHBAR_ABOTTOM = 1654
ID_MENU_VIEW_TREE = 1660
ID_MENU_VIEW_TREE_ALEFT = 1661
ID_MENU_VIEW_TREE_ARIGHT = 1662
ID_TOOLBAR_CHANNEL = 1401
ID_TOOLBAR_TOOLS = 1401

class frame_main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "%s %s" % (circe_globals.APPNAME, circe_globals.VERSION), wx.DefaultPosition, wx.Size(600,  400)) 
        self.CreateStatusBar()
        self.SetStatusText("Welcome to %s version %s (%s)" % (circe_globals.APPNAME,  circe_globals.VERSION, circe_globals.APPTAG))
        
        self.toolbar_Channels = None
        
        self.create_controls()
        self.create_menu()
        self.create_sizers()
        self.create_switch_bar()
        self.create_tree()
        self.bind_events()
        self.add_controls()

        # Run a little test for the window area and the switchbar
        #self.testWindow = wx.TextCtrl(self.panel_window_area,-1,"Test Window Area. (Window 1)",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow2 = wx.TextCtrl(self.panel_window_area,-1,"Test Window Area. (Window 2)",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow3 = wx.TextCtrl(self.panel_window_area,-1,"Test Window Area. (Window 3)",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow = window_channel(self.panel_window_area,-1,"Window 1")
        #self.testWindow2 = window_channel(self.panel_window_area,-1,"Window 2")
        #self.testWindow3 = window_channel(self.panel_window_area,-1,"Window 3")
        #self.panel_window_area.AddWindow(self.testWindow,self.testWindow.GetCaption())
        #self.panel_window_area.AddWindow(self.testWindow2,self.testWindow2.GetCaption())
        #self.panel_window_area.AddWindow(self.testWindow3,self.testWindow3.GetCaption())
        #self.panel_window_area.show_window(self.testWindow)
        # Create two servers + status windows
        s = servermanager.add_server(self.panel_window_area)
        #w = window_status(self.panel_window_area,s,-1)
        #s2 = servermanager.add_server(self.panel_window_area)
        #w2 = window_status(self.panel_window_area,s2,-1)
        #self.panel_window_area.AddWindow(w)
        #self.panel_window_area.AddWindow(w2)
        self.panel_window_area.show_window(s.statuswindow.section_id,s.statuswindow)
        
    def create_menu(self):
        menu_file = wx.Menu() 
        menu_file.Append(ID_MENU_FILE_ABOUT, "&About", "About %s" % (circe_globals.APPNAME))
        menu_file.AppendSeparator()
        menu_file.Append(ID_MENU_FILE_EXIT, "E&xit", "Exit %s" % (circe_globals.APPNAME))
        
        menu_switchbar = wx.Menu()
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ALEFT, "Align switch_bar &Left")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ARIGHT, "Align switch_bar &Right")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ATOP, "Align switch_bar &Top")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ABOTTOM, "Align switch_bar &Bottom")
        
        menu_tree = wx.Menu()
        menu_tree.Append(ID_MENU_VIEW_TREE_ALEFT, "Align Tree &Left")
        menu_tree.Append(ID_MENU_VIEW_TREE_ARIGHT, "Align Tree &Right")
        
        menu_view = wx.Menu()
        menu_view.AppendMenu(ID_MENU_VIEW_SWITCHBAR, "&switch_bar", menu_switchbar)
        menu_view.AppendMenu(ID_MENU_VIEW_TREE, "&Treebar", menu_tree)
        
        menu_bar = wx.MenuBar() 
        menu_bar.Append(menu_file, "&File");
        menu_bar.Append(menu_view, "&View");

        self.SetMenuBar(menu_bar)
        
        wx.EVT_MENU(self, ID_MENU_FILE_ABOUT, self.evt_menu_About)
        wx.EVT_MENU(self, ID_MENU_FILE_EXIT, self.evt_menu_Exit)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ALEFT, self.evt_menu_switchbar_align_left)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ARIGHT, self.evt_menu_switchbar_align_right)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ATOP, self.evt_menu_switchbar_align_top)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ABOTTOM, self.evt_menu_switchbar_align_bottom)
        wx.EVT_MENU(self, ID_MENU_VIEW_TREE_ALEFT, self.evt_menu_tree_align_left)
        wx.EVT_MENU(self, ID_MENU_VIEW_TREE_ARIGHT, self.evt_menu_tree_align_right)

    def create_switch_bar(self):
        sbsize = (circe_config.switchbar_hsize,circe_config.switchbar_vsize)
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            sbalign = wx.VERTICAL
        else:
            sbalign = wx.HORIZONTAL
        self.panel_switch_bar = panel_switchbar(self.panel_top,-1,sbsize,sbalign)
        # Temporary, until we find some decent way to interact with
        # panel_window_area about servers
        self.panel_switch_bar.add_section(0)
    
    def align_switch_bar(self):
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            sbalign = wx.VERTICAL
            sbsize = (circe_config.switchbar_hsize,-1)
        else:
            sbalign = wx.HORIZONTAL
            sbsize = (-1,circe_config.switchbar_vsize)
        self.panel_switch_bar.set_alignment(sbalign,sbsize)

    def create_tree(self):
        self.panel_Tree = panel_tree(self.panel_top,-1,circe_config.tree_size)

    def create_controls(self):
        self.panel_top = wx.Panel(self,-1)
        self.panel_window_area = panel_windowarea(self.panel_top,-1)

    def bind_events(self):
        self.panel_switch_bar.bind_click(self.evt_switchbar_event)
        self.panel_window_area.bind_add(self.evt_windowarea_addwindow)
        self.panel_window_area.bind_del(self.evt_windowarea_delwindow)
        self.panel_window_area.bind_show(self.evt_windowarea_showwindow)
        self.panel_window_area.bind_set_caption(self.evt_windowarea_setcaption)
    
    def realize(self):
        self.destroy_sizers()
        self.create_sizers()
        self.add_controls()
        self.Refresh(True)
        self.panel_window_area.Refresh(True)
    
    def destroy_sizers(self):
        self.sizer_top.Clear(False)
        self.sizer_top.Destroy()
    
    def create_sizers(self):
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            self.sizer_top = wx.BoxSizer()
        else:
            self.sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_tree_and_window_area = wx.BoxSizer()
        self.panel_top.SetSizer(self.sizer_top,False)

    def add_controls(self):
        # switch_bar
        if (circe_config.switchbar_position == wx.LEFT or circe_config.switchbar_position == wx.TOP) and circe_config.switchbar_show == True:
            self.sizer_top.Add(self.panel_switch_bar,0,wx.EXPAND)
        self.sizer_top.Add(self.sizer_tree_and_window_area,1,wx.EXPAND)
        if (circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.BOTTOM) and circe_config.switchbar_show == True:
            self.sizer_top.Add(self.panel_switch_bar,0,wx.EXPAND)
        # Tree
        if circe_config.tree_position == wx.LEFT and circe_config.tree_show == True:
            self.sizer_tree_and_window_area.Add(self.panel_Tree,0,wx.EXPAND)
        # Windowarea
        self.sizer_tree_and_window_area.Add(self.panel_window_area,1,wx.EXPAND)
        # Tree
        if circe_config.tree_position == wx.RIGHT and circe_config.tree_show == True:
            self.sizer_tree_and_window_area.Add(self.panel_Tree,0,wx.EXPAND)

        # Hide disabled controls
        if not circe_config.tree_show:
            self.panel_Tree.Show(False)
        if not circe_config.switchbar_show:
            self.panel_switch_bar.Show(False)
        self.panel_top.Layout()
    
    def rebuild_switch_bar(self):
        self.align_switch_bar()
        self.realize()

    def rebuild_tree(self):
        self.realize()

    def evt_menu_About(self,event):
        wx.MessageBox(circe_globals.APPNAME + " version " + circe_globals.VERSION,"About")
    
    def evt_menu_Exit(self,event):
        self.Close()
    
    def evt_menu_switchbar_align_left(self,event):
        circe_config.switchbar_position = wx.LEFT
        self.rebuild_switch_bar()

    def evt_menu_switchbar_align_right(self,event):
        circe_config.switchbar_position = wx.RIGHT
        self.rebuild_switch_bar()

    def evt_menu_switchbar_align_top(self,event):
        circe_config.switchbar_position = wx.TOP
        self.rebuild_switch_bar()

    def evt_menu_switchbar_align_bottom(self,event):
        circe_config.switchbar_position = wx.BOTTOM
        self.rebuild_switch_bar()

    def evt_menu_tree_align_left(self,event):
        circe_config.tree_position = wx.LEFT
        self.rebuild_tree()

    def evt_menu_tree_align_right(self,event):
        circe_config.tree_position = wx.RIGHT
        self.rebuild_tree()

    def evt_switchbar_event(self,section_id,button_id):
        self.panel_window_area.show_window(section_id,button_id,True)

    def evt_windowarea_addwindow(self,section_id,window_id,caption,type=None):
        self.panel_switch_bar.add_button(section_id,window_id,caption)

    def evt_windowarea_delwindow(self,section_id,window_id):
        self.panel_switch_bar.remove_button(section_id,window_id)

    def evt_windowarea_showwindow(self,section_id,window_id):
        self.panel_switch_bar.select(section_id,window_id)

    def evt_windowarea_setcaption(self,section_id,window_id,caption):
        self.panel_switch_bar.set_caption(section_id,window_id,caption)
