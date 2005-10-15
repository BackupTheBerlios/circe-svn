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
from window_base import WindowTextEdit


class WindowStatus(WindowTextEdit):
    def __init__(self,windowarea,server):
        WindowTextEdit.__init__(self, windowarea, server, "Status")

        self.windowarea.add_window(server,self)
        self.section_id = server
        
        self.server = server
        # Whether to check regularly for new events or not
        self.checking = False
        # Delay between each checking (in ms)
        self.timer_delay = 500
        
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
    
    def create_sizers(self):
        self.sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer_top)
    
    def add_controls(self):
        self.sizer_top.Add(self.txt_buffer,1,wx.EXPAND)
        self.sizer_top.Add(self.txt_edit,0,wx.EXPAND)

    def enable_checking(self):
        """Turn on checking for new events."""
        if self.checking:
            return
        self.timer = wx.Timer(self)
        self.timer.Start(self.timer_delay)
        self.checking = True
        if self.server.debug:
            print "Automatic checking for new events enabled"

    def disable_checking(self):
        """Turn off checking for new events."""
        if not self.checking:
            return
        self.timer.Stop()
        del self.timer
        self.checking = False
        if self.server.debug:
            print "Automatic checking for new events disabled"

    def OnTimerEvt(self, evt):
        if not self.server.is_connected():
            self.disable_checking()
            return
        self.server.check_events()

    def ischecking(self):
        """Returns True if checking for new events is enabled otherwise False.
        """
        return self.checking

    def evt_disconnect(self):
        # Disable checking
        self.disable_checking()
        # Duplicate channel list
        channellist = list(self.server.channels)
        # Close all channels
        for chan in channellist:
            chan.close()

    # GUI events.
