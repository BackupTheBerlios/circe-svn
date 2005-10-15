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
import os, sys

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
        menu_file.AppendSeparator()
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
        self.Bind(wx.EVT_CLOSE, self.evt_window_del)

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

    def evt_window_del(self,*a):
        for server in servermanager.servers: 
            try:    
                server.connection.quit(circe_globals.QUITMSG)
            except:
                pass
        sys.exit()

class About(wxPython.wx.wxDialog):
    def __init__(self,event):
        windowname = "About "+circe_globals.APPNAME+" "+circe_globals.VERSION
        wx.Dialog.__init__(self, None, -1, windowname, style=wx.DEFAULT_DIALOG_STYLE)

        self.notebook = wx.Notebook(self, -1, size=(100,110))

        self.main_panel = wx.Panel(self.notebook)
        self.credits_panel = wx.Panel(self.notebook)
        self.license_panel = wx.Panel(self.notebook)
        self.other_panel = wx.Panel(self.notebook)

        self.notebook.AddPage(self.main_panel, "About "+circe_globals.APPNAME)
        self.notebook.AddPage(self.credits_panel, "Credits")
        self.notebook.AddPage(self.license_panel, "License")
        self.notebook.AddPage(self.other_panel, "Other")

        self.dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dialog_sizer.Add(self.notebook, -1, wx.EXPAND, 5)
        self.SetSizer(self.dialog_sizer)

        self.OK_button = wx.Button(self, 100, "Ok",(-1,-1), wx.DefaultSize)
        self.dialog_sizer.Add(self.OK_button, 0, wx.CENTER)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_panel.SetSizer(self.main_sizer)

        self.credits_sizer = wx.BoxSizer(wx.VERTICAL)
        self.credits_panel.SetSizer(self.credits_sizer)

        self.license_sizer = wx.BoxSizer(wx.VERTICAL)
        self.license_panel.SetSizer(self.license_sizer)

        self.other_sizer = wx.BoxSizer(wx.VERTICAL)
        self.other_panel.SetSizer(self.other_sizer)

        self.about_text = "%s %s\nPython IRC Client\n%s\n" % (circe_globals.APPNAME, circe_globals.VERSION, circe_globals.HOMEPAGE)
        self.about_text_dlg = wx.TextCtrl(self.main_panel, -1,"",wx.DefaultPosition,(60,60),wx.TE_MULTILINE|wx.TE_CENTRE)
        self.about_text_dlg.AppendText(self.about_text)
        self.about_text_dlg.SetEditable(0)

        self.bitmap = wx.StaticBitmap(self.main_panel, -1)
        self.bitmap.SetBitmap(wx.BitmapFromImage(wx.Image(os.path.join("images", "circe.png"), wx.BITMAP_TYPE_PNG)))

        self.main_sizer.Add(self.bitmap,1,wx.CENTER)
        self.main_sizer.Add(self.about_text_dlg, 2, wx.LEFT|wx.EXPAND|wx.ALL)

        self.credits_text = open("doc/CREDITS.txt").read()
        self.credits_text_dlg = wx.TextCtrl(self.credits_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.credits_text_dlg.AppendText(self.credits_text)
        self.credits_text_dlg.SetEditable(0)
        self.credits_sizer.Add(self.credits_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)
      
        self.license_text = open("doc/LICENSE_IMPORTED.txt").read()
        self.license_text_dlg = wx.TextCtrl(self.license_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.license_text_dlg.AppendText(self.license_text)
        self.license_text_dlg.SetEditable(0)
        self.license_sizer.Add(self.license_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)

        import irclib 
        irclib_version = ""
        for VerStr in irclib.VERSION: irclib_version += str(VerStr)+"." 
        python_version = "%s.%s.%s %s" % (sys.version_info[0], sys.version_info[1], sys.version_info[2], sys.version_info[3])

        self.other_text = "%s Version: %s\nPython Version: %s\nWxPython Version: %s\npython-irclib Version: %s\n" % (circe_globals.APPNAME, \
                                                                                               circe_globals.VERSION, \
                                                                                               python_version, wx.VERSION_STRING, irclib_version[:5])
        self.other_text_dlg = wx.TextCtrl(self.other_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.other_text_dlg.AppendText(self.other_text)
        self.other_text_dlg.SetEditable(0)
        self.other_sizer.Add(self.other_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)

        wxPython.wx.EVT_BUTTON(self,100,self.OnClick)        
        
        self.ShowModal()
    
    def OnClick(self, *a):
        self.Destroy() 
