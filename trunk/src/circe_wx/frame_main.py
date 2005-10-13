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

# Imports
# System
import wx, wxPython
from wx.lib.dialogs import ScrolledMessageDialog
import os

# Circe
import circe_globals
import config as circe_config
import servermanager
from panel_switchbar import PanelSwitchbar
from panel_windowarea import PanelWindowarea
from panel_tree import PanelTree
from window_channel import WindowChannel
from window_status import WindowStatus

ID_MENU_FILE_NEWSERVER = wx.NewId()
ID_MENU_HELP_ABOUT = wx.NewId()
ID_MENU_FILE_EXIT = wx.NewId()

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
        self.create_switchbar()
        self.create_tree()
        self.bind_events()
        self.add_controls()

        # Create a server + a status window
        s = servermanager.add_server(self.panel_windowarea)
        self.panel_windowarea.show_window(s.statuswindow.section_id,s.statuswindow)
        
    def create_menu(self):
        menu_file = wx.Menu()
        menu_file.Append(ID_MENU_FILE_NEWSERVER, "New &server", "Create a new server tab.")
        menu_file.Append(ID_MENU_FILE_EXIT, "E&xit", "Exit %s" % (circe_globals.APPNAME))
        menu_help = wx.Menu()
        menu_help.Append(ID_MENU_HELP_ABOUT, "&About", "About %s" % (circe_globals.APPNAME))
        
        menu_bar = wx.MenuBar() 
        menu_bar.Append(menu_file, "&File")
        menu_bar.Append(menu_help, "&Help")

        self.SetMenuBar(menu_bar)
        
        wx.EVT_MENU(self, ID_MENU_HELP_ABOUT, About)
        wx.EVT_MENU(self, ID_MENU_FILE_EXIT, self.evt_menu_Exit)
        wx.EVT_MENU(self, ID_MENU_FILE_NEWSERVER, self.evt_menu_NewServer)
    def create_switchbar(self):
        sbsize = (circe_config.switchbar_hsize,circe_config.switchbar_vsize)
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            sbalign = wx.VERTICAL
        else:
            sbalign = wx.HORIZONTAL
        self.panel_switchbar = PanelSwitchbar(self.panel_top,-1,sbsize,sbalign)
    
    def align_switchbar(self):
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            sbalign = wx.VERTICAL
            sbsize = (circe_config.switchbar_hsize,-1)
        else:
            sbalign = wx.HORIZONTAL
            sbsize = (-1,circe_config.switchbar_vsize)
        self.panel_switchbar.set_alignment(sbalign,sbsize)

    def create_tree(self):
        self.panel_Tree = PanelTree(self.panel_top,-1,circe_config.tree_size)

    def create_controls(self):
        self.panel_top = wx.Panel(self,-1)
        self.panel_windowarea = PanelWindowarea(self.panel_top,-1)

    def bind_events(self):
        self.panel_switchbar.bind_click(self.evt_switchbar_event)
        self.panel_windowarea.bind_add(self.evt_windowarea_addwindow)
        self.panel_windowarea.bind_del(self.evt_windowarea_delwindow)
        self.panel_windowarea.bind_show(self.evt_windowarea_showwindow)
        self.panel_windowarea.bind_set_caption(self.evt_windowarea_setcaption)
    
    def realize(self):
        self.destroy_sizers()
        self.create_sizers()
        self.add_controls()
        self.Refresh(True)
        self.panel_windowarea.Refresh(True)
    
    def destroy_sizers(self):
        self.sizer_top.Clear(False)
        self.sizer_top.Destroy()
    
    def create_sizers(self):
        if circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT:
            self.sizer_top = wx.BoxSizer()
        else:
            self.sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_tree_and_windowarea = wx.BoxSizer()
        self.panel_top.SetSizer(self.sizer_top,False)

    def add_controls(self):
        # switch_bar
        if (circe_config.switchbar_position == wx.LEFT or circe_config.switchbar_position == wx.TOP) and circe_config.switchbar_show == True:
            self.sizer_top.Add(self.panel_switchbar,0,wx.EXPAND)
        self.sizer_top.Add(self.sizer_tree_and_windowarea,1,wx.EXPAND)
        if (circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.BOTTOM) and circe_config.switchbar_show == True:
            self.sizer_top.Add(self.panel_switchbar,0,wx.EXPAND)
        # Tree
        if circe_config.tree_position == wx.LEFT and circe_config.tree_show == True:
            self.sizer_tree_and_windowarea.Add(self.panel_Tree,0,wx.EXPAND)
        # Windowarea
        self.sizer_tree_and_windowarea.Add(self.panel_windowarea,1,wx.EXPAND)
        # Tree
        if circe_config.tree_position == wx.RIGHT and circe_config.tree_show == True:
            self.sizer_tree_and_windowarea.Add(self.panel_Tree,0,wx.EXPAND)

        # Hide disabled controls
        if not circe_config.tree_show:
            self.panel_Tree.Show(False)
        if not circe_config.switchbar_show:
            self.panel_switchbar.Show(False)
        self.panel_top.Layout()
    
    def rebuild_switchbar(self):
        self.align_switchbar()
        self.realize()

    def rebuild_tree(self):
        self.realize()

    def evt_menu_About(self,event):
        data = []
        data.append("%s version %s\n" % (circe_globals.APPNAME, circe_globals.VERSION))
        data.append("Site: %s\n" % (circe_globals.HOMEPAGE))
        data.append(circe_globals.IMPORTANT_DATA)

        dialog = ScrolledMessageDialog(self, ''.join(data), "About")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.logo = wx.BitmapFromImage(wx.Image(os.path.join("images","circe.png"), wx.BITMAP_TYPE_PNG))
        self.bitmap = wx.StaticBitmap(dialog, -1)
        self.bitmap.SetBitmap(self.logo)

        sizer.Add(self.bitmap)
        sizer.Add(dialog)

#        sizer.Fit(dialog)
#        dialog.SetSizer(sizer)
        dialog.Show()

    def evt_menu_Exit(self,event):
        self.Close()

    def evt_menu_NewServer(self, event):
        s = servermanager.add_server(self.panel_windowarea)
        self.panel_windowarea.show_window(s.statuswindow.section_id,s.statuswindow)

    def evt_switchbar_event(self,section_id,button_id):
        self.panel_windowarea.show_window(section_id,button_id,True)

    def evt_windowarea_addwindow(self,section_id,window_id,caption,type=None):
        self.panel_switchbar.add_button(section_id,window_id,caption)

    def evt_windowarea_delwindow(self,section_id,window_id):
        self.panel_switchbar.remove_button(section_id,window_id)

    def evt_windowarea_showwindow(self,section_id,window_id):
        self.panel_switchbar.select(section_id,window_id)

    def evt_windowarea_setcaption(self,section_id,window_id,caption):
        self.panel_switchbar.set_caption(section_id,window_id,caption)

class About(wxPython.wx.wxDialog):
	def __init__(self,event):
		wxPython.wx.wxDialog.__init__ (self,None,-1, 'About Circe', size = (200,200))
		self.panel = wxPython.wx.wxPanel(self, -1)
	        self.logo = wx.BitmapFromImage(wx.Image(os.path.join("images","circe.png"), wx.BITMAP_TYPE_PNG))
	        self.bitmap = wx.StaticBitmap(self.panel, -1)
	        self.bitmap.SetBitmap(self.logo)
		self.appname_label = wxPython.wx.wxStaticText(self.panel, -1, "%s %s\n" % (circe_globals.APPNAME, circe_globals.VERSION))
		self.ok_button = wxPython.wx.wxButton(self.panel, 100,"Ok")
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.bitmap, 0, wxPython.wx.wxALIGN_CENTER)
		self.sizer.Add(self.ok_button, 1, wxPython.wx.wxALIGN_CENTER)
		self.panel.SetSizerAndFit(self.sizer)
		self.sizer.Fit(self)
		wxPython.wx.EVT_BUTTON(self.panel, 100, self.click)
		self.ShowModal()
	def click(self,event):
		self.EndModal(wx.ID_OK)

