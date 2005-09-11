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
from irclib import nm_to_n

import lorem
from window_base import WindowTextEdit

ID_LST_USERS = wx.NewId()

class WindowChannel(WindowTextEdit):
    def __init__(self,windowarea,server,channelname):
        WindowTextEdit.__init__(self, windowarea, server, channelname)
        self.windowarea = windowarea
        
        self.channelname = channelname
        self._users = {} # Store info about users
        
        self.create_controls()
        self.create_sizers()
        self.add_controls()

        self.windowarea.add_window(server,self)

    def get_channelname(self):
        return self.channelname

    def create_controls(self):
        self.lst_users = wx.ListCtrl(self,ID_LST_USERS, 
                                    style=wx.LC_REPORT
                                    | wx.LC_SORT_ASCENDING
                                    | wx.LC_NO_HEADER
                                    )
        self.lst_users.InsertColumn(0, "Users")

    def create_sizers(self):
        self.sizer_top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_buffer_andusers = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer_top)

    def add_controls(self):
        self.sizer_buffer_andusers.Add(self.txt_buffer,1,wx.EXPAND)
        self.sizer_buffer_andusers.Add(self.lst_users,0,wx.EXPAND)
        self.sizer_top.Add(self.sizer_buffer_andusers,1,wx.EXPAND)
        self.sizer_top.Add(self.txt_edit,0,wx.EXPAND)


    def users(self, users=[]):
        """Update the uers list and eventually add the given users."""
        if users:
            for u in users:
                if u not in self._users.keys():
                    self._users[u] = ""

        self.lst_users.DeleteAllItems()
        for u in self._users.keys():
            self.lst_users.Append((u,))

    def del_user(self, users):
        """Delete some users from the users list.

        Arguments:
            users -- either a string or a list of strings representing the
                     user(s) name(s).
        """
        if not isinstance(users, list):
            users = [users]

        # Deletes left users.
        for u in self._users.keys():
            if u in users:
                del self._users[u]
        self.users()


    def user_quit(self, event):
        """Remove a users from the list and informs that the user has quit."""

        # Ensures this is a quit event.
        if event.eventtype() != "quit":
            return

        user = nm_to_n(event.source())

        if user in self._users.keys():
            self.del_user(user)
            self.server_event("%s has quit: %s" % (user, event.arguments()))


    def add_message(self, text, from_, to=""):
        """Format a message in a pretty way with the given arguments.

        Arguments:
            text  -- the content of the message
            from_ -- the sender of the message
            to    -- (Optional) target of the message
        """
        if to:
            to = "(to %s)" % to	
        message = "<%s %s> %s" % (from_, to, text)
        self.server_event(message)

    # GUI events.
    def evt_closed(self):
        WindowTextEdit.evt_closed(self)
        self.server.channel_closed(self)
