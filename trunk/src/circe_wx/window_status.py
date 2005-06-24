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
#from windowserver import windowserver
from window_base import WindowTextEdit

ID_TXT_EDIT = wx.NewId()

class WindowStatus(WindowTextEdit):
    def __init__(self,windowarea,server):
        #server.SetStatusWindow(self)
#        windowserver.__init__(self,windowarea,server,"Status")
        WindowTextEdit.__init__(self, windowarea, server, "Status")

        self.windowarea.add_window(server,self)
        self.section_id = server
        
        self.server = server
        # Whether to check regularly for new events or not
        self.checking = False
        # Delay between each checking (in ms)
        self._timer_delay = 500
        
        self.create_controls()
        self.create_sizers()
        self.add_controls()

        # Bind EVT_TIMER events to self.OnTimerEvt
        self.Bind(wx.EVT_TIMER, self.OnTimerEvt)

    def make_caption(self):
        if self.server.get_host():
            caption = self.server.get_host()
        else:
            caption = "Not connected"
        return caption
    
    def create_controls(self):
        self.txt_edit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)
        #self.txt_edit.Bind(wx.EVT_CHAR, self.txt_edit_evt_char)
        wx.EVT_CHAR(self.txt_edit,self.txt_edit_evt_char)
    
    def create_sizers(self):
        self.sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer_top)
    
    def add_controls(self):
        self.sizer_top.Add(self.txt_buffer,1,wx.EXPAND)
        self.sizer_top.Add(self.txt_edit,0,wx.EXPAND)

    def txt_edit_evt_char(self, event):
        key = event.GetKeyCode()
        if key == 13:
            # Enter pressed
            value = self.txt_edit.GetValue()
            self.txt_edit.SetValue("")
            self.server.text_command(value,self)
            # Do nothing after this! We might be destroyed!
        else:
            event.Skip()

    def enable_checking(self):
        """Turns on checking for new events."""
        if self.checking:
            return
        self.timer = wx.Timer(self)
        self.timer.Start(self._timer_delay)
        self.checking = True
        if self.server.debug:
            print "Automatic checking for new events enabled"

    def disable_checking(self):
        """Turns off checking for new events."""
        if not self.checking:
            return
        self.timer.Stop()
        del self.timer
        self.checking = False
        if self.server.debug:
            print "Automatic checking for new events disabled"

    def OnTimerEvt(self, evt):
        if not self.server.is_connected():
            self.disablechecking()
            return
        self.server.check_events()

    def ischecking(self):
        """Returns True if checking for new events is enabled otherwise False.
        """
        return self.checking

    def evt_disconnect(self):
        # Disable checking
        self.disablechecking()
        # Duplicate channel list
        channellist = []
        for chan in self.server.channels:
            channellist.append(chan)
        # Close all channels
        for chan in channellist:
            chan.close_window()

    # Events
    def evt_focus(self):
        self.txt_edit.SetFocus()
