import wx
from window_channel import window_channel

class panel_windowarea(wx.Panel):
    def __init__(self,parent,panelID):
        wx.Panel.__init__(self,parent,panelID)
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        #self.testArea = wx.TextCtrl(self,-1,"Test Window Area.\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.testArea = window_channel(self,-1)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.testArea,1,wx.EXPAND)