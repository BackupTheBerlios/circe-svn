import wx

class panel_window(wx.Panel):
    def __init__(self,parent,windowID):
        wx.Panel.__init__(self,parent,windowID)
        print "Window created! ID:",windowID