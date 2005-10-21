import os
import sys
import wx
import circe_globals

class AboutDialog(wx.Dialog):
    def __init__(self):
        windowname = "About %s %s" % (circe_globals.APPNAME, circe_globals.VERSION)
        wx.Dialog.__init__(self, None, -1, windowname, style=wx.DEFAULT_DIALOG_STYLE, size=(370,205))

        self.notebook = wx.Notebook(self, -1, size=(100,110))

        self.main_panel = wx.Panel(self.notebook)
        self.credits_panel = wx.Panel(self.notebook)
        self.license_panel = wx.Panel(self.notebook)
        self.other_panel = wx.Panel(self.notebook)

        self.notebook.AddPage(self.main_panel, "About %s" % circe_globals.APPNAME)
        self.notebook.AddPage(self.credits_panel, "Credits")
        self.notebook.AddPage(self.license_panel, "License")
        self.notebook.AddPage(self.other_panel, "Other")

        self.dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dialog_sizer.Add(self.notebook, -1, wx.EXPAND, 5)
        self.SetSizer(self.dialog_sizer)

        self.OK_button = wx.Button(self, 100, "Ok",(-1,-1), wx.DefaultSize)
        self.dialog_sizer.Add(self.OK_button, 0, wx.CENTER)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_panel.SetSizer(self.main_sizer)

        self.credits_sizer = wx.BoxSizer(wx.VERTICAL)
        self.credits_panel.SetSizer(self.credits_sizer)

        self.license_sizer = wx.BoxSizer(wx.VERTICAL)
        self.license_panel.SetSizer(self.license_sizer)

        self.other_sizer = wx.BoxSizer(wx.VERTICAL)
        self.other_panel.SetSizer(self.other_sizer)

        self.about_text = "%s %s\nPython IRC Client\n%s\n" % (circe_globals.APPNAME, circe_globals.VERSION, circe_globals.HOMEPAGE)
        self.about_text_dlg = wx.TextCtrl(self.main_panel, -1,"",wx.DefaultPosition,(60,60),wx.TE_MULTILINE|wx.TE_CENTRE)
        self.about_text_dlg.AppendText(self.about_text)
        self.about_text_dlg.SetEditable(0)

        self.bitmap = wx.StaticBitmap(self.main_panel, -1)
        self.bitmap.SetBitmap(wx.BitmapFromImage(wx.Image(os.path.join("images", "circe.png"), wx.BITMAP_TYPE_PNG)))

        self.main_sizer.Add(self.bitmap,1,wx.CENTER)
        self.main_sizer.Add(self.about_text_dlg, 2, wx.LEFT|wx.EXPAND|wx.ALL)

        self.credits_text = open("doc/CREDITS.txt").read()
        self.credits_text_dlg = wx.TextCtrl(self.credits_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.credits_text_dlg.AppendText(self.credits_text)
        self.credits_text_dlg.SetEditable(0)
        self.credits_sizer.Add(self.credits_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)
      
        self.license_text = open("doc/LICENSE_IMPORTED.txt").read()
        self.license_text_dlg = wx.TextCtrl(self.license_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.license_text_dlg.AppendText(self.license_text)
        self.license_text_dlg.SetEditable(0)
        self.license_sizer.Add(self.license_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)

        import irclib 
        irclib_version = ".".join(map(str, irclib.VERSION))
        python_version = ".".join(map(str, sys.version_info[:3]))
        python_version += (" " + sys.version_info[3])

        self.other_text = "%s Version: %s\nPython Version: %s\nWxPython Version: %s\npython-irclib Version: %s\n" % (circe_globals.APPNAME, \
                                                                                               circe_globals.VERSION, \
                                                                                               python_version, wx.VERSION_STRING, irclib_version[:5])

        self.other_text_dlg = wx.TextCtrl(self.other_panel, -1,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE|wx.TE_CENTRE)
        self.other_text_dlg.AppendText(self.other_text)
        self.other_text_dlg.SetEditable(0)
        self.other_sizer.Add(self.other_text_dlg, 1, wx.CENTER|wx.EXPAND|wx.ALL)

        wx.EVT_BUTTON(self,100,self.OnClick)        
    
    def OnClick(self, *a):
        self.Destroy() 