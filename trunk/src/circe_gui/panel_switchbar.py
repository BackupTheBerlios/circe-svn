import wx

class panel_switchbar(wx.Panel):
    def __init__(self,parent,panelID,barsize=-1,baralign=wx.TB_HORIZONTAL):
        self.barsize = barsize
        self.baralign = baralign
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.barsize)
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        #wx.ToolBar(self,-1,wx.DefaultPosition,wx.DefaultSize,self.barlign)
        self.testBar = wx.TextCtrl(self,-1,"Test Switchbar Area",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.testBar,1,wx.EXPAND)