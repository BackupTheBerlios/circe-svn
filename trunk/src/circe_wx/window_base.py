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
        self.txt_edit = wx.TextCtrl(self,ID_TXT_EDIT,"",wx.DefaultPosition,wx.DefaultSize,wx.TE_PROCESS_TAB)

        self.txt_buffer = wx.TextCtrl(self,-1,"",wx.DefaultPosition,
                wx.DefaultSize,wx.TE_MULTILINE)
        self.txt_buffer.SetEditable(False)
        f = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Monospace")
        self.txt_buffer.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.NullColour, f))

        self.txt_edit.Bind(wx.EVT_CHAR, self.txt_edit_evt_char)
        
        # Command history
        self.historysize = 10 # TODO: Get this from config
        self.history = [] # History buffer, first item is the last entered command
        self.currenthistory = -1 # -1 means we're not navigating the history
        self.currentcommand = "" # This is the text entered in the input box before navigating history
    
    def set_input(self,text):
        """Sets input box to text"""
        self.txt_edit.SetValue(text)
        self.txt_edit.SetInsertionPointEnd()
    
    def get_input(self):
        """Returns input box value"""
        return self.txt_edit.GetValue()
    
    def enter(self):
        """Executed when the user presses enter"""
        value = self.txt_edit.GetValue()
        if not value: # ignore event if nothing typed
            return
        self.history_add(value)
        self.set_input("")
        self.set_currentcommand("")
        self.current_area_up = 0
        self.current_area_down = 0
        self.server.text_command(value,self)
        # Do nothing after this! We might be destroyed!
    
    def set_currentcommand(self,value):
        """Sets the current command to a new value, resets history navigation"""
        self.currentcommand = value
        self.currenthistory = -1
    
    def return_to_currentcommand(self):
        """Returns current input to before browsing the history"""
        self.set_input(self.currentcommand)
        self.currenthistory = -1
    
    def check_history_changed(self):
        """Finds out if the user has changed the history item"""
        if self.currenthistory < 0:
            return False
        old = self.history[self.currenthistory]
        new = self.get_input()
        if cmp(new,old) == 0:
            # History unchanged
            return False
        else:
            # History changed
            self.set_currentcommand(self.get_input())
            return True
    
    def history_add(self,text):
        """Add history item"""
        self.history.insert(0,text)
        if len(self.history) > self.historysize:
            # Exceeded max history length
            self.history.pop()

    def history_back(self):
        """Go back in time"""
        if not self.check_history_changed():
            if self.currenthistory == -1:
                # We were at the beginning, store current command
                self.set_currentcommand(self.get_input())
            if self.currenthistory+1 == len(self.history):
                # Last item, do nothing
                pass
            else:
                # Moving back in time
                self.currenthistory += 1
                self.set_input(self.history[self.currenthistory])
    
    def history_forward(self):
        """Go forwards in time"""
        if not self.check_history_changed():
            if self.currenthistory < 0:
                # We were at the beginning, store current command
                self.set_currentcommand(self.get_input())
                return
            if self.currenthistory == 0:
                # We have arrived at the beginning, show current command
                self.return_to_currentcommand()
            else:
                # Moving forwards in time
                self.currenthistory -= 1
                self.set_input(self.history[self.currenthistory])
    
    def autocomplete(self):
        """Autocompletes the current input"""
        value = self.txt_edit.GetValue()
        if not value: # ignore if nothing typed
            return
        get_channelname  = getattr(self, "get_channelname", None)
        if not get_channelname: # ignore if cannot get channel name
            return
        channel = get_channelname() # get the channel name
        if not channel or channel == "debug": # is it none, or is it debug? ignore
            return

        window = self.server.get_channel_window(channel)
        users = window._users 
        value_s = value.split(" ")[-1]
        for user in users:
            if user.startswith(value_s):
                if len(value.split(" ")) <= 1:
                    self.txt_edit.SetValue(user+": ")
                    self.txt_edit.SetInsertionPointEnd()
                    break
                else:
                    txt = self.txt_edit.GetValue().split(" ")
                    txt = " ".join(txt[:len(txt)-1])
                    self.txt_edit.SetValue(txt+" "+user+" ")
                    self.txt_edit.SetInsertionPointEnd()
                    break

    def server_event(self, event):
        """Display an event in the text buffer."""
        self.txt_buffer.AppendText(event+"\n")

    # GUI events.
    def evt_focus(self):
        self.txt_edit.SetFocus()

    def txt_edit_evt_char(self, event):
        """Called when the user presses a key."""
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN or key == wx.WXK_NUMPAD_ENTER: # enter
            self.enter()
        elif key == wx.WXK_UP: # up
            self.history_back()
        elif key == wx.WXK_DOWN: # down
            self.history_forward()
        elif key == wx.WXK_TAB: # tab
            self.autocomplete()
        else: # Process this key
            event.Skip()

    def txt_buffer_clr(self, *a):
        """clear the text buffer"""
        self.txt_buffer.SetValue("")
