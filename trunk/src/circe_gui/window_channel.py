import wx
from panel_window import panel_window

class window_channel(panel_window):
    def OnCreate(self):
        print "Channel window created"
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        self.testArea = wx.TextCtrl(self,-1,"Test Channel Area.\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.testArea,1,wx.EXPAND)