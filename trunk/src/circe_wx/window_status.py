# Circe
# Copyright (C) 2004-2005 The Circe development team

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import wx
from window_server import window_server

ID_TXT_EDIT = wx.NewId()

class window_status(window_server):
    def __init__(self,windowarea,server):
        #server.SetStatusWindow(self)
        window_server.__init__(self,windowarea,server,"Status")

        self.windowarea.AddWindow(server,self)
        self.section_id = server
        
        self._server = server
        # Whether to check regularly for new events or not
        self._checking = False
        # Delay between each checking (in ms)
        self._timer_delay = 500
        
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()

        # Bind EVT_TIMER events to self.OnTimerEvt
        self.Bind(wx.EVT_TIMER, self.OnTimerEvt)

    def MakeCaption(self):
        if self.server.getHost():
            caption = self.server.getHost()
        else:
            caption = "Not connected"
        return caption
    
    def CreateControls(self):
        self.txtEdit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)
        #self.txtEdit.Bind(wx.EVT_CHAR, self.txtEdit_EvtChar)
        wx.EVT_CHAR(self.txtEdit,self.txtEdit_EvtChar)
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        self.sizer_Top.Add(self.txtBuffer,1,wx.EXPAND)
        self.sizer_Top.Add(self.txtEdit,0,wx.EXPAND)

    def txtEdit_EvtChar(self, event):
        key = event.GetKeyCode()
        if key == 13:
            # Enter pressed
            #self.TextCommand(self.txtEdit.GetValue())
            self.server.TextCommand(self.txtEdit.GetValue(),self)
            self.txtEdit.SetValue("")
        else:
            event.Skip()

    def enableChecking(self):
        """Turns on checking for new events."""
        if self._checking:
            return
        self.timer = wx.Timer(self)
        self.timer.Start(self._timer_delay)
        self._checking = True
        if self._server._debug:
            print "Automatic checking for new events enabled"

    def disableChecking(self):
        """Turns off checking for new events."""
        if not self._checking:
            return
        self.timer.Stop()
        del self.timer
        self._checking = False
        if self._server._debug:
            print "Automatic checking for new events disabled"

    def OnTimerEvt(self, evt):
        if not self._server.is_connected():
            self.disableChecking()
            return
        self._server.checkEvents()

    def isChecking(self):
        """Returns True if checking for new events is enabled otherwise False.
        """
        return self._checking
