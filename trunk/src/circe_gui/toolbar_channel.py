import wx

class toolbar_channel(wx.ToolBar):
    def __init__(self,parent,tbID,align=wx.TB_HORIZONTAL):
        wx.ToolBar.__init__(self,parent,tbID,wx.DefaultPosition,wx.DefaultSize,align)