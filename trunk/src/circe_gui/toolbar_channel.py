import wx

class toolbar_channel(wx.ToolBar):
    def __init__(self,parent,tbID,size=wx.DefaultSize,align=wx.TB_HORIZONTAL):
        wx.ToolBar.__init__(self,parent,tbID,wx.DefaultPosition,size,align)