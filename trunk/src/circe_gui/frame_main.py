import wx
import circe_globals
import circe_config
from circe_gui.panel_switchbar import panel_switchbar
from circe_gui.panel_windowarea import panel_windowarea
from circe_gui.panel_tree import panel_tree

ID_MENU_FILE_ABOUT = 1001
ID_MENU_FILE_EXIT = 1002
ID_MENU_VIEW_SWITCHBAR_ALEFT = 1651
ID_MENU_VIEW_SWITCHBAR_ARIGHT = 1652
ID_MENU_VIEW_SWITCHBAR_ATOP = 1653
ID_MENU_VIEW_SWITCHBAR_ABOTTOM = 1654
ID_MENU_VIEW_TREE_ALEFT = 1661
ID_MENU_VIEW_TREE_ARIGHT = 1662
ID_TOOLBAR_CHANNEL = 1401
ID_TOOLBAR_TOOLS = 1401

class frame_main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, circe_globals.APPNAME + " " + circe_globals.VERSION, wx.DefaultPosition, wx.Size(600,  400)) 
        self.CreateStatusBar()
        self.SetStatusText("Welcome to " + circe_globals.APPNAME + " version " + circe_globals.VERSION + " (" + circe_globals.APPTAG + ")") 
        
        self.toolbar_Channels = None
        
        self.CreateControls()
        self.CreateMenu()
        self.CreateSizers()
        self.CreateSwitchBar()
        self.CreateTree()
        self.AddControls()
        
    def CreateMenu(self):
        menu_file = wx.Menu() 
        menu_file.Append(ID_MENU_FILE_ABOUT, "&About", "About " + circe_globals.APPNAME)
        menu_file.AppendSeparator()
        menu_file.Append(ID_MENU_FILE_EXIT, "E&xit", "Exit " + circe_globals.APPNAME)
        
        menu_switchbar = wx.Menu()
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ALEFT, "Align Switchbar &Left")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ARIGHT, "Align Switchbar &Right")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ATOP, "Align Switchbar &Top")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ABOTTOM, "Align Switchbar &Bottom")
        
        menu_tree = wx.Menu()
        menu_tree.Append(ID_MENU_VIEW_TREE_ALEFT, "Align Tree &Left")
        menu_tree.Append(ID_MENU_VIEW_TREE_ARIGHT, "Align Tree &Right")
        
        menu_view = wx.Menu()
        menu_view.AppendMenu(-1, "&Switchbar", menu_switchbar)
        menu_view.AppendMenu(-1, "&Treebar", menu_tree)
        
        menuBar = wx.MenuBar() 
        menuBar.Append(menu_file, "&File");
        menuBar.Append(menu_view, "&View");

        self.SetMenuBar(menuBar)
        
        wx.EVT_MENU(self, ID_MENU_FILE_ABOUT, self.evt_menu_About)
        wx.EVT_MENU(self, ID_MENU_FILE_EXIT, self.evt_menu_Exit)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ALEFT, self.evt_menu_switchbar_align_left)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ARIGHT, self.evt_menu_switchbar_align_right)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ATOP, self.evt_menu_switchbar_align_top)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ABOTTOM, self.evt_menu_switchbar_align_bottom)
        wx.EVT_MENU(self, ID_MENU_VIEW_TREE_ALEFT, self.evt_menu_tree_align_left)
        wx.EVT_MENU(self, ID_MENU_VIEW_TREE_ARIGHT, self.evt_menu_tree_align_right)

    def CreateSwitchBar(self):
        if(circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT):
            sbalign = wx.VERTICAL
            sbsize = (circe_config.switchbar_hsize,-1)
        else:
            sbalign = wx.HORIZONTAL
            sbsize = (-1,circe_config.switchbar_vsize)
        self.panel_Switchbar = panel_switchbar(self.panel_Top,-1,sbsize,sbalign)
    
    def AlignSwitchbar(self):
        if(circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT):
            sbalign = wx.VERTICAL
            sbsize = (circe_config.switchbar_hsize,-1)
        else:
            sbalign = wx.HORIZONTAL
            sbsize = (-1,circe_config.switchbar_vsize)
        self.panel_Switchbar.SetAlignment(sbalign,sbsize)

    def CreateTree(self):
        self.panel_Tree = panel_tree(self.panel_Top,-1,circe_config.tree_size)

    def CreateControls(self):
        self.panel_Top = wx.Panel(self,-1)
        self.panel_WindowArea = panel_windowarea(self.panel_Top,-1)
    
    def DestroySizers(self):
        del self.sizer_Top
        del self.sizer_TreeAndWindowArea
    
    def CreateSizers(self):
        if(circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT):
            self.sizer_Top = wx.BoxSizer()
        else:
            self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_TreeAndWindowArea = wx.BoxSizer()
        self.panel_Top.SetSizer(self.sizer_Top)

    def AddControls(self):
        # Switchbar
        if((circe_config.switchbar_position == wx.LEFT or circe_config.switchbar_position == wx.TOP) and circe_config.switchbar_show == True):
            self.sizer_Top.Add(self.panel_Switchbar,0,wx.EXPAND)
        self.sizer_Top.Add(self.sizer_TreeAndWindowArea,1,wx.EXPAND)
        if((circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.BOTTOM) and circe_config.switchbar_show == True):
            self.sizer_Top.Add(self.panel_Switchbar,0,wx.EXPAND)
        # Tree
        if(circe_config.tree_position == wx.LEFT and circe_config.tree_show == True):
            self.sizer_TreeAndWindowArea.Add(self.panel_Tree,0,wx.EXPAND)
        # Windowarea
        self.sizer_TreeAndWindowArea.Add(self.panel_WindowArea,1,wx.EXPAND)
        # Tree
        if(circe_config.tree_position == wx.RIGHT and circe_config.tree_show == True):
            self.sizer_TreeAndWindowArea.Add(self.panel_Tree,0,wx.EXPAND)
        self.panel_Top.Layout()
    
    def RebuildSwitchBar(self):
        self.DestroySizers()
        self.CreateSizers()
        self.AlignSwitchbar()
        self.AddControls()
        self.Layout()

    def RebuildTree(self):
        self.DestroySizers()
        self.CreateSizers()
        self.AddControls()
        self.Layout()


    def evt_menu_About(self,event):
        wx.MessageBox(circe_globals.APPNAME + " version " + circe_globals.VERSION,"About")
    
    def evt_menu_Exit(self,event):
        self.Close()
    
    def evt_menu_switchbar_align_left(self,event):
        circe_config.switchbar_position = wx.LEFT
        self.RebuildSwitchBar()

    def evt_menu_switchbar_align_right(self,event):
        circe_config.switchbar_position = wx.RIGHT
        self.RebuildSwitchBar()

    def evt_menu_switchbar_align_top(self,event):
        circe_config.switchbar_position = wx.TOP
        self.RebuildSwitchBar()

    def evt_menu_switchbar_align_bottom(self,event):
        circe_config.switchbar_position = wx.BOTTOM
        self.RebuildSwitchBar()

    def evt_menu_tree_align_left(self,event):
        circe_config.tree_position = wx.LEFT
        self.RebuildTree()

    def evt_menu_tree_align_right(self,event):
        circe_config.tree_position = wx.RIGHT
        self.RebuildTree()