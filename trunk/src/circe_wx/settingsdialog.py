import wx
import circe_config
import config_engine

class SettingsDialog(wx.Dialog):
    def __init__(self): 
        wx.Dialog.__init__(self, None, -1, "Settings", wx.DefaultPosition, wx.DefaultSize)

        self.notebook = wx.Notebook(self, -1)
  
        self.General_tab = wx.Panel(self.notebook)
        self.Servers_tab = wx.Panel(self.notebook)

        self.notebook.AddPage(self.General_tab, "General")
        self.notebook.AddPage(self.Servers_tab, "Servers")

        self.dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.General_sizer = wx.BoxSizer(wx.VERTICAL)
        self.Servers_sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.dialog_sizer)
        self.General_tab.SetSizer(self.General_sizer)
        self.Servers_tab.SetSizer(self.Servers_sizer)

        self.dialog_sizer.Add(self.notebook, -1, wx.EXPAND|wx.ALIGN_TOP, 5)
        self.dialog_sizer.Add(self.buttons_sizer, 0, flag=wx.ALIGN_RIGHT)
        self.buttons_sizer.Layout()

        self.OK_button = wx.Button(self, 100, "Ok",(-1,-1), wx.DefaultSize)
        self.CANCEL_button = wx.Button(self, 101, "Cancel", (-1,-1), wx.DefaultSize)

        self.buttons_sizer.Add(self.OK_button, proportion=0, flag=wx.ALIGN_RIGHT)
        self.buttons_sizer.Add(self.CANCEL_button, proportion=0, flag=wx.ALIGN_RIGHT)

        # START MASSIVE CONTROLS ADDITIONS (OMG!! ITS COMING!! HELLS FREEZING OVER!! :o)
 
        self.General_DNickTxt = wx.StaticText(self.General_tab, -1, "Default Nickname: ")
        self.General_DNickEnt = wx.TextCtrl(self.General_tab, -1, "")



        self.config = config_engine.Config()
