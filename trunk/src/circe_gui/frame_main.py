import wx
import circe_globals
import circe_config
from circe_gui.toolbar_channel import toolbar_channel
from circe_gui.panel_windowarea import panel_windowarea
from circe_gui.panel_tree import panel_tree

ID_MENU_FILE_ABOUT = 1001
ID_MENU_FILE_EXIT = 1002
ID_MENU_VIEW_SWITCHBAR_ALEFT = 1651
ID_MENU_VIEW_SWITCHBAR_ARIGHT = 1652
ID_MENU_VIEW_SWITCHBAR_ATOP = 1653
ID_MENU_VIEW_SWITCHBAR_ABOTTOM = 1654
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
        
        menu_view = wx.Menu()
        menu_view.AppendMenu(-1, "&Switchbar", menu_switchbar)
        
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

    def CreateSwitchBar(self):
        if(circe_config.switchbar_show == True):
            if(circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT):
                self.toolbar_Channels = wx.Button(self.panel_Top,-1,"Test Switchbar",wx.DefaultPosition,(circe_config.switchbar_hsize,-1))
                #self.toolbar_Channels = toolbar_channel(self.panel_Top,ID_TOOLBAR_CHANNEL,wx.TB_VERTICAL)
            else:
                self.toolbar_Channels = wx.Button(self.panel_Top,-1,"Test Switchbar",wx.DefaultPosition,(-1,circe_config.switchbar_vsize))
                #self.toolbar_Channels = toolbar_channel(self.panel_Top,ID_TOOLBAR_CHANNEL)
    
    def DestroySwitchBar(self):
        self.toolbar_Channels.Destroy()

    def CreateTree(self):
        if(circe_config.tree_show == True):
            self.panel_Tree = panel_tree(self.panel_Top,-1,circe_config.tree_size)

    def DestroyTree(self):
        self.panel_Tree.Destroy()

    def CreateControls(self):
        self.panel_Top = wx.Panel(self,-1)
        #self.panel_WindowArea = wx.TextCtrl(self.panel_Top,-1,"Test Window Area.\nModify circe_config.switchbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.panel_WindowArea = panel_windowarea(self.panel_Top,-1)

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
            self.sizer_Top.Add(self.toolbar_Channels,0,wx.EXPAND)
        self.sizer_Top.Add(self.sizer_TreeAndWindowArea,1,wx.EXPAND)
        if((circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.BOTTOM) and circe_config.switchbar_show == True):
            self.sizer_Top.Add(self.toolbar_Channels,0,wx.EXPAND)
        # Tree
        if(circe_config.tree_position == wx.LEFT and circe_config.tree_show == True):
            self.sizer_TreeAndWindowArea.Add(self.panel_Tree,0,wx.EXPAND)
        # Windowarea
        self.sizer_TreeAndWindowArea.Add(self.panel_WindowArea,1,wx.EXPAND)
        # Tree
        if(circe_config.tree_position == wx.RIGHT and circe_config.tree_show == True):
            self.sizer_TreeAndWindowArea.Add(self.panel_Tree,0,wx.EXPAND)
        #self.panel_WindowArea.AddControls()
        self.panel_Top.Layout()
    
    def ConfigControls(self):
        if(circe_config.switchbar_position == wx.RIGHT or circe_config.switchbar_position == wx.LEFT):
            self.toolbar_Channels.SetSize((-1,circe_config.switchbar_vsize))
        else:
            self.toolbar_Channels.SetSize((circe_config.switchbar_hsize,-1))
    
    def RebuildSwitchBar(self):
        self.sizer_Top.Clear(False)
        self.CreateSizers()
        self.DestroySwitchBar()
        self.CreateSwitchBar()
        self.AddControls()
        self.panel_Top.Layout()

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