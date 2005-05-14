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
import lorem
from window_server import window_server
from irclib import nm_to_n

ID_TXT_EDIT = wx.NewId()
ID_LST_USERS = wx.NewId()

class window_channel(window_server):
    def __init__(self,windowarea,server,channelname):
        window_server.__init__(self,windowarea,server,channelname)
        self.windowarea = windowarea
        
        self._channelname = channelname
        self._users = {} # Store info about users
        
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()

        self.windowarea.AddWindow(server,self)

    def getChannelname(self):
        return self._channelname

    def CreateControls(self):
        self.txtEdit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)
        self.lstUsers = wx.ListCtrl(self,ID_LST_USERS, 
                                    style=wx.LC_REPORT
                                    | wx.LC_SORT_ASCENDING
                                    | wx.LC_NO_HEADER
                                    )
        self.lstUsers.InsertColumn(0, "Users")
        wx.EVT_CHAR(self.txtEdit,self.txtEdit_EvtChar)

    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(wx.VERTICAL)
        self.sizer_BufferAndUsers = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer_Top)

    def AddControls(self):
        self.sizer_BufferAndUsers.Add(self.txtBuffer,1,wx.EXPAND)
        self.sizer_BufferAndUsers.Add(self.lstUsers,0,wx.EXPAND)
        self.sizer_Top.Add(self.sizer_BufferAndUsers,1,wx.EXPAND)
        self.sizer_Top.Add(self.txtEdit,0,wx.EXPAND)

    def txtEdit_EvtChar(self, event):
        key = event.GetKeyCode()
        if key == 13:
            # Enter pressed
            self.server.TextCommand(self.txtEdit.GetValue(),self)
            self.txtEdit.SetValue("")
        else:
            event.Skip()

    def users(self, users=[]):
        """Adds some users to the users list and update it."""
        if users:
            for u in users:
                if u not in self._users.keys():
                    self._users[u] = ""

        self.lstUsers.DeleteAllItems()
        for u in self._users.keys():
            self.lstUsers.Append((u,))

    def delUsers(self, users):
        """Deletes some users from the users list.

        Arguments:

            users -- either a string or a list of strings representing the
                     user(s) name(s).

        """
        if type(users) != type([]):
            users = [users]

        # Deletes left users.
        for u in self._users.keys():
            if u in users:
                del self._users[u]
        self.users()


    def userQuit(self, event):
        """Removes a users from the list and informs that the user has quit."""

        # Ensures this is a quit event.
        if event.eventtype() != "quit":
            return

        user = nm_to_n(event.source())

        if user in self._users.keys():
            self.delUsers(user)
            self.ServerEvent("%s has quit: %s" % (user, event.arguments()[0]))


    def addMessage(self, text, from_, to=""):
        """Formats a message in a pretty way with the given arguments.

        Arguments:

            text  -- the content of the message
            from_ -- the sender of the message
            to    -- (Optional) target of the message

        """
        if to:
            to = "(to %s)" % to
        message = "<%s%s> %s" % (from_, to, text)
        self.ServerEvent(message)

    # Events
    def evt_focus(self):
        self.txtEdit.SetFocus()
