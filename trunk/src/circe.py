import wx
from circe_gui.frame_main import frame_main

class CirceApp(wx.App): 
    def OnInit(self): 
        self.mainFrame = frame_main()
        self.mainFrame.Show(True)
        self.SetTopWindow(self.mainFrame)
        return True

if(__name__ == "__main__"):
    circe = CirceApp(0)
    circe.MainLoop()