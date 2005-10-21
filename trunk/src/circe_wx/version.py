import wx
import circe_globals
import urllib2

def CheckVersion(showcurrent=True):
    GCVout = GetCurrentVersion()    

    if GCVout == 0:
        if showcurrent:
            text = "You are currently running the latest version of %s." % (circe_globals.APPNAME)
            wx.MessageBox(text, "No Updates Available", wx.OK|wx.ICON_INFORMATION)
    else: 
        text = "You are currently running an old version of %s. The currently available version is %s. \nWould you like to visit the %s homepage? " % (circe_globals.APPNAME, GCVout, circe_globals.APPNAME)
        result = wx.MessageBox(text,"Updates Available!", wx.YES_NO|wx.ICON_EXCLAMATION)
        if result == wx.YES: import webbrowser; webbrowser.open(circe_globals.HOMEPAGE, new=1)

def GetCurrentVersion():
    a = urllib2.urlopen("http://circe.berlios.de/version.php")
    curver2 = a.read()
    curver = curver2.split(".")
    runver = circe_globals.VERSION.split(".")

    if curver[2] > runver[2]: # minor version difference:
        return curver2 # OLD!!
    elif curver[1] > runver[1]: # old middle version difference:
        return curver2 # OLD!!
    elif curver[0] > runver[0]: # major version difference:
        return curver2
    else:
        return 0