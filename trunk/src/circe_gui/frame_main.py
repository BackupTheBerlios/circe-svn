import wx
import circe_globals
import circe_config
from circe_gui.toolbar_channel import toolbar_channel

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
        
        self.CreateMenu()
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateMenu(self):
        menu_file = wx.Menu() 
        menu_file.Append(ID_MENU_FILE_ABOUT, "&About", "About " + circe_globals.APPNAME)
        menu_file.AppendSeparator()
        menu_file.Append(ID_MENU_FILE_EXIT, "E&xit", "Exit " + circe_globals.APPNAME)
        
        menu_switchbar = wx.Menu()
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ALEFT, "Align Switchbar Left")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ARIGHT, "Align Switchbar Right")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ATOP, "Align Switchbar Top")
        menu_switchbar.Append(ID_MENU_VIEW_SWITCHBAR_ABOTTOM, "Align Switchbar Bottom")
        
        menu_view = wx.Menu()
        menu_view.AppendMenu(-1, "&Switchbar", menu_switchbar)
        
        menuBar = wx.MenuBar() 
        menuBar.Append(menu_file, "&File");
        menuBar.Append(menu_view, "&View");

        self.SetMenuBar(menuBar)
        
        wx.EVT_MENU(self, ID_MENU_FILE_ABOUT, self.evt_menu_About)
        wx.EVT_MENU(self, ID_MENU_FILE_EXIT, self.evt_menu_Exit)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ALEFT, self.evt_menu_switchbar_align)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ARIGHT, self.evt_menu_switchbar_align)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ATOP, self.evt_menu_switchbar_align)
        wx.EVT_MENU(self, ID_MENU_VIEW_SWITCHBAR_ABOTTOM, self.evt_menu_switchbar_align)

    def CreateControls(self):
        self.TopPanel = wx.Panel(self,-1)
        if(circe_config.toolbarposition == wx.RIGHT or circe_config.toolbarposition == wx.LEFT):
            self.toolbar_Channels = wx.Button(self.TopPanel,-1,"Test Toolbar")
            #self.toolbar_Channels = toolbar_channel(self.TopPanel,ID_TOOLBAR_CHANNEL,wx.TB_VERTICAL)
        else:
            self.toolbar_Channels = wx.Button(self.TopPanel,-1,"Test Toolbar")
            #self.toolbar_Channels = toolbar_channel(self.TopPanel,ID_TOOLBAR_CHANNEL)

    def CreateSizers(self):
        if(circe_config.toolbarposition == wx.RIGHT or circe_config.toolbarposition == wx.LEFT):
            self.sizer_Top = wx.BoxSizer()
        else:
            self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_TreeAndWindowArea = wx.BoxSizer()
        self.TopPanel.SetSizer(self.sizer_Top)

    def AddControls(self):
        if(circe_config.toolbarposition == wx.LEFT or circe_config.toolbarposition == wx.TOP):
            self.sizer_Top.Add(self.toolbar_Channels,0,wx.EXPAND)
            self.sizer_Top.Add(self.sizer_TreeAndWindowArea,1,wx.EXPAND)
        else:
            self.sizer_Top.Add(self.sizer_TreeAndWindowArea,1,wx.EXPAND)
            self.sizer_Top.Add(self.toolbar_Channels,0,wx.EXPAND)
        self.sizer_TreeAndWindowArea.Add(wx.TextCtrl(self.TopPanel,-1,"Test Window Area.\nModify circe_config.toolbarposition to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE),1,wx.EXPAND)
        self.TopPanel.Layout()

    def evt_menu_About(self,event):
        wx.MessageBox(circe_globals.APPNAME + " version " + circe_globals.VERSION,"About")
    
    def evt_menu_Exit(self,event):
        self.Close()
    
    def evt_menu_switchbar_align(self,event):
        pass