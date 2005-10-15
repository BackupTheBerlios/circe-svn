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
from panel_window import PanelWindow

ID_TXT_EDIT = wx.NewId()

class WindowServer(PanelWindow):
    def __init__(self,windowarea,server,caption=None):
        self.windowarea = windowarea
        self.server = server
        PanelWindow.__init__(self,windowarea,caption)

    def get_windowarea(self):
        return self.windowarea

    def get_server(self):
        return self.server

    def evt_caption(self):
        self.windowarea.set_caption(self.server,self,self.caption)



class WindowTextEdit(WindowServer):
    """A window that contains a TextCtrl and convenient methods to add some
    text.
    """
    def __init__(self, windowarea, server, channelname):
        WindowServer.__init__(self, windowarea, server, channelname)

        # Controls (not in a create_controls() method otherwise it is
        # overridden by subclasses.
        self.txt_edit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize)

        self.txt_buffer = wx.TextCtrl(self,-1,"",wx.DefaultPosition,
                wx.DefaultSize,wx.TE_MULTILINE)
        self.txt_buffer.SetEditable(False)
        f = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Monospace")
        self.txt_buffer.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.NullColour, f))

        self.txt_edit.Bind(wx.EVT_CHAR, self.txt_edit_evt_char)


    def txt_edit_evt_char(self, event):
        """Called when the user enter some text in the entry widget."""
        key = event.GetKeyCode()
        if key == 13:
            # Enter pressed
            value = self.txt_edit.GetValue()
            self.txt_edit.SetValue("")
            self.server.text_command(value,self)
            # Do nothing after this! We might be destroyed!
        else:
            event.Skip()


    def server_event(self, event):
        """Display an event in the text buffer."""
        self.txt_buffer.AppendText(event+"\n")


    # GUI events.
    def evt_focus(self):
        self.txt_edit.SetFocus()

    def txt_buffer_clr(self, *a):
        """clear the text buffer"""
	self.txt_buffer.SetValue("")
