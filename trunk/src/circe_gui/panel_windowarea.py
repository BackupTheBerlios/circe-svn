import wx
from window_channel import window_channel

class panel_windowarea(wx.Panel):
    def __init__(self,parent,panelID):
        wx.Panel.__init__(self,parent,panelID)
        self.windowList = []
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
        self.testWindow = wx.TextCtrl(self,-1,"Test Window Area. (Window 1)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.testWindow2 = wx.TextCtrl(self,-1,"Test Window Area. (Window 2)\nModify circe_config.toolbar_position to change toolbar alignment.",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        #self.testWindow = window_channel(self,-1)
        #self.testWindow2 = window_channel(self,-1)
        self.AddWindow(self.testWindow)
        self.AddWindow(self.testWindow2)
        self.ShowWindow(self.testWindow)
        self.ShowWindow(self.testWindow2)
    
    def AddWindow(self,window):
        if(window in self.windowList):
            raise "Window already exists"
        else:
            self.windowList.append(window)
            window.Show(False)
    
    def RemoveWindow(self,window):
        if(window in self.windowList):
            self.sizer_Top.Remove(window)
            self.windowList[self.windowList.index(window)] = None
        else:
            raise "Window does not exist in windows list"
    
    def ShowWindow(self,window):
        if(window in self.windowList):
            for winToHide in self.windowList:
                winToHide.Show(False)
                self.sizer_Top.Remove(winToHide)
            window.Show(True)
            self.sizer_Top.Add(window,1,wx.EXPAND)
            self.sizer_Top.Layout()
        else:
            raise "Window does not exist in windows list"
    
    def CreateControls(self):
        pass
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer()
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        pass