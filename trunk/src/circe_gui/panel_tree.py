import wx

class panel_tree(wx.Panel):
    def __init__(self,parent,panelID,treesize=-1):
        self.treesize = (treesize,-1)
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.treesize)
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        self.testArea = wx.TextCtrl(self,-1,"Test Tree Area",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.testArea,1,wx.EXPAND)