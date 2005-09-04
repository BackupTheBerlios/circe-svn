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
import circe_config
import wx.lib.buttons as genbuttons

class SwitchSection:
    def __init__(self,section_id,parent):
        self.section_id = section_id
        self.buttons = {}
        self.parent = parent
    
    def add_button(self,button_id,text,icon=None):
        if button_id in self.buttons:
            raise "Button %s already exists in section %s" % (button_id, self.section_id)
        else:
            self.buttons[button_id] = SwitchButton(self.section_id,button_id,self.parent,text,icon)
            self.buttons[button_id].Show(False)
            # Bind event
            #print "Binding with: ",self.buttons[button_id].event_id
            wx.EVT_BUTTON(self.parent,self.buttons[button_id].event_id,self.button_event)
    
    def remove_button(self,button_id):
        if button_id in self.buttons:
            self.buttons[button_id].Destroy()
            del self.buttons[button_id]
        else:
            raise "Button %s does not exist in section %s" % (button_id, self.section_id)

    def set_caption(self,button_id,caption):
        if button_id in self.buttons:
            self.buttons[button_id].set_caption(caption)
        else:
            raise "Button %s does not exist in section %s" % (button_id, self.section_id)
    
    def remove_all(self):
        for button_id,button in self.buttons.iteritems():
            button.Destroy()
            del self.buttons[button_id]
    
    def button_event(self,event):
        for button_id,button in self.buttons.iteritems():
            if button.event_id == event.GetId():
                # We found our event button
                self.parent.button_event(self.section_id,button.button_id)

class SwitchButton(genbuttons.GenBitmapTextToggleButton):
    def __init__(self,section_id,button_id,parent,text,icon=None):
        self.button_id = button_id
        self.event_id = int(wx.NewId())
        self.icon = icon
        self.parent = parent
        self.previous_button = None
        genbuttons.GenBitmapTextToggleButton.__init__(self,parent,self.event_id,icon,text)
        self.SetUseFocusIndicator(False)

        # Here begins code to change button behaviour
        # The button will instantly trigger when the it is depressed
        wx.EVT_LEFT_DOWN(self,self.OnLeftDown_Override)
        wx.EVT_LEFT_UP(self,self.OnLeftUp_Override)
        wx.EVT_LEFT_DCLICK(self,self.OnDClick_Override)

    def set_caption(self,caption):
        self.SetLabel(caption)

    def OnLeftDown_Override(self,event):
        self.OnLeftDown(event)
        self.OnLeftUp(event)

    def OnLeftUp_Override(self,event):
        pass

    def OnDClick_Override(self,event):
        self.OnLeftDown(event)
        self.OnLeftUp(event)
    
class PanelSwitchbar(wx.Panel):
    def __init__(self,parent,panelID,barsize,baralign=wx.HORIZONTAL,autosec=True):
        self.barsize = barsize
        self.baralign = baralign
        self.sections = {}
        self.autosection = autosec # Automatically adds and deletes sections
        self.currentbutton = None
        self.func_click = None
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.barsize)
        
        self.create_sizers()
        
        #self.add_controls()
        #self.Layout()
        self.realize()

        wx.EVT_SIZE(self,self.OnSize)
    
    def realize(self):
        """Make all changes effective and layout the window"""
        self.remove_controls()
        self.destroy_sizers()
        self.create_sizers()
        self.add_controls()
        self.Layout()
    
    def add_section(self,section_id):
        """Add a section"""
        if section_id in self.sections:
            raise "Section %s already exists" % section_id
        else:
            self.sections[section_id] = SwitchSection(section_id,self)
    
    def remove_section(self,section_id):
        """Remove a section"""
        if section_id in self.sections:
            self.sections[section_id].remove_all()
            del self.sections[section_id]
        else:
            raise "Section %s does not exist" % section_id
    
    def add_button(self,section_id,button_id,text,icon=None):
        """Add a button"""
        if section_id in self.sections:
            self.sections[section_id].add_button(button_id,text,icon)
            self.realize()
        else:
            if self.autosection:
                self.add_section(section_id)
                self.add_button(section_id,button_id,text,icon)
            else:
                raise "Section %s does not exist" % section_id
    
    def remove_button(self,section_id,button_id):
        """Remove a button"""
        if section_id in self.sections:
            self.sections[section_id].remove_button(button_id)
            if self.autosection:
                if len(self.sections[section_id].buttons) == 0:
                    self.remove_section(section_id)
        else:
            raise "Section %s does not exist" % section_id

    def set_caption(self,section_id,button_id,text):
        """Add a button"""
        if section_id in self.sections:
            self.sections[section_id].set_caption(button_id,text)
            self.realize()
        else:
            raise "Section %s does not exist" % section_id
    
    def set_alignment(self,baralign,barsize):
        self.SetSize(barsize)
        self.baralign = baralign
        self.realize()
    
    def destroy_sizers(self):
        """Destroy sizer"""
        self.sizer_top.Clear(False)
        self.sizer_top.Destroy()
    
    def create_sizers(self):
        """Create sizer"""
        self.sizer_top = wx.BoxSizer(self.baralign)
        self.SetSizer(self.sizer_top,False)
        
    def add_controls(self):
        """Add all controls to the sizer"""
        if (self.baralign == wx.HORIZONTAL):
            fill = 1
            self.sizer_top.Add((0,self.barsize[1]))
        else:
            fill = 0
            self.sizer_top.Add((self.barsize[0],0))
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_top.Add(button,fill,wx.EXPAND)
                button.Show(True)
            self.sizer_top.Add((10,10))
    
    def remove_controls(self):
        """Remove all controls from the sizer"""
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_top.Remove(button)
                
    def get_button(self,section_id,button_id):
        """Get a button object"""
        for active_section_id,section in self.sections.iteritems():
            if active_section_id == section_id:
                for active_button_id,button in section.buttons.iteritems():
                    if active_button_id == button_id:
                        return button
        return None # Not found
    
    def unselect_all_except(self,section_id,button_id):
        """Unselect all buttons except the one specified"""
        for active_section_id,section in self.sections.iteritems():
                for active_button_id,button in section.buttons.iteritems():
                    if not(active_button_id == button_id and active_section_id == section_id):
                        button.SetValue(False)
    
    def select_button(self,section_id,button_id):
        """select a button without deselecting anything"""
        button = self.get_button(section_id,button_id)
        if button != None:
            button.SetValue(True)
            return True
        return False

    def select(self,section_id,button_id):
        """select a button and deselects everything else, this doesn't raise an event"""
        button = self.get_button(section_id,button_id)
        self.unselect_all_except(section_id,button_id)
        self.select_button(section_id,button_id)
        button.previous_button = self.currentbutton
        self.currentbutton = [section_id,button_id]
    
    def toggle_button(self,section_id,button_id):
        """Check if button is pressed, if it is NOT, select previous button"""
        button = self.get_button(section_id,button_id)
        if button.GetValue():
            # Clicked a new button
            self.unselect_all_except(section_id,button_id)
            button.previous_button = self.currentbutton
            self.currentbutton = [section_id,button_id]
        else :
            # Clicked the current button
            if button.previous_button != None:
                if self.select_button(button.previous_button[0],button.previous_button[1]):
                    self.currentbutton = [button.previous_button[0],button.previous_button[1]]
                else:
                    # The previous button wasn't found
                    button.previous_button = None
                    button.SetValue(True)
            else:
                button.SetValue(True)

    def button_event(self,section_id,button_id):
        """Called whenever a button is clicked"""
        #print "Button event: section_id:",section_id," button_id:", button_id
        self.toggle_button(section_id,button_id)
        if self.func_click is not None:
            self.func_click(self.currentbutton[0],self.currentbutton[1])

    def bind_click(self,func):
        """Bind a function to a Click event"""
        self.func_click = func

    def OnSize(self,event):
        """The Size event needs to be overloaded to hard-Refresh the buttons"""
        self.Layout()
        self.Refresh()
