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

class PanelWindow(wx.Panel):
    def __init__(self,windowarea,caption):
        wx.Panel.__init__(self,windowarea,-1)
        self.windowarea = windowarea
        self.caption = caption

    def get_caption(self):
        return self.caption

    def set_caption(self,cap):
        self.caption = cap
        self.evt_caption()

    def close(self):
        self.evt_closed()
        self.windowarea.remove_window(self.server,self)
        self.Destroy()

    # Events
    def evt_closed(self):
        pass

    def evt_caption(self):
        pass

    def evt_focus(self):
        pass
