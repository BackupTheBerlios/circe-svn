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

class switchsection:
    def __init__(self,section_id,parent):
        self.section_id = section_id
        self.buttons = {}
        self.parent = parent
    
    def AddButton(self,button_id,text,icon=None):
        if button_id in self.buttons:
            raise "Button %s already exists in section %s" % (button_id, self.section_id)
        else:
            self.buttons[button_id] = switchbutton(self.section_id,button_id,self.parent,text,icon)
            self.buttons[button_id].Show(False)
            # Bind event
            #print "Binding with: ",self.buttons[button_id].event_id
            wx.EVT_BUTTON(self.parent,self.buttons[button_id].event_id,self.ButtonEvent)
    
    def RemoveButton(self,button_id):
        if button_id in self.buttons:
            self.buttons[button_id].Destroy()
            del self.buttons[button_id]
        else:
            raise "Button %s does not exist in section %s" % (button_id, self.section_id)

    def SetCaption(self,button_id,caption):
        if button_id in self.buttons:
            self.buttons[button_id].SetCaption(caption)
        else:
            raise "Button %s does not exist in section %s" % (button_id, self.section_id)
    
    def RemoveAll(self):
        for button_id,button in self.buttons.iteritems():
            button.Destroy()
            del self.buttons[button_id]
    
    def ButtonEvent(self,event):
        for button_id,button in self.buttons.iteritems():
            if button.event_id == event.GetId():
                # We found our event button
                self.parent.ButtonEvent(self.section_id,button.button_id)

class switchbutton(genbuttons.GenBitmapTextToggleButton):
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

    def SetCaption(self,caption):
        self.SetLabel(caption)

    def OnLeftDown_Override(self,event):
        self.OnLeftDown(event)
        self.OnLeftUp(event)

    def OnLeftUp_Override(self,event):
        pass

    def OnDClick_Override(self,event):
        self.OnLeftDown(event)
        self.OnLeftUp(event)
    
class panel_switchbar(wx.Panel):
    def __init__(self,parent,panelID,barsize,baralign=wx.HORIZONTAL,autosec=True):
        self.barsize = barsize
        self.baralign = baralign
        self.sections = {}
        self.autosection = autosec # Automatically adds and deletes sections
        self.currentbutton = None
        self.func_click = None
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.barsize)
        
        self.CreateSizers()
        
        #self.AddControls()
        #self.Layout()
        self.Realize()

        wx.EVT_SIZE(self,self.OnSize)
    
    def Realize(self):
        """Makes all changes effective and layouts the window"""
        self.RemoveControls()
        self.DestroySizers()
        self.CreateSizers()
        self.AddControls()
        self.Layout()
    
    def AddSection(self,section_id):
        """Adds a section"""
        if section_id in self.sections:
            raise "Section %s already exists" % section_id
        else:
            self.sections[section_id] = switchsection(section_id,self)
    
    def RemoveSection(self,section_id):
        """Removes a section"""
        if section_id in self.sections:
            self.sections[section_id].RemoveAll()
            del self.sections[section_id]
        else:
            raise "Section %s does not exist" % section_id
    
    def AddButton(self,section_id,button_id,text,icon=None):
        """Adds a button"""
        if section_id in self.sections:
            self.sections[section_id].AddButton(button_id,text,icon)
            self.Realize()
        else:
            if self.autosection:
                self.AddSection(section_id)
                self.AddButton(section_id,button_id,text,icon)
            else:
                raise "Section %s does not exist" % section_id
    
    def RemoveButton(self,section_id,button_id):
        """Removes a button"""
        if section_id in self.sections:
            self.sections[section_id].RemoveButton(button_id)
            if self.autosection:
                if len(self.sections[section_id].buttons) == 0:
                    self.RemoveSection(section_id)
        else:
            raise "Section %s does not exist" % section_id

    def SetCaption(self,section_id,button_id,text):
        """Adds a button"""
        if section_id in self.sections:
            self.sections[section_id].SetCaption(button_id,text)
            self.Realize()
        else:
            raise "Section %s does not exist" % section_id
    
    def SetAlignment(self,baralign,barsize):
        self.SetSize(barsize)
        self.baralign = baralign
        self.Realize()
    
    def DestroySizers(self):
        """Destroys sizer"""
        self.sizer_Top.Clear(False)
        self.sizer_Top.Destroy()
    
    def CreateSizers(self):
        """Creates sizer"""
        self.sizer_Top = wx.BoxSizer(self.baralign)
        self.SetSizer(self.sizer_Top,False)
        
    def AddControls(self):
        """Adds all controls to the sizer"""
        if (self.baralign == wx.HORIZONTAL):
            fill = 1
            self.sizer_Top.Add((0,self.barsize[1]))
        else:
            fill = 0
            self.sizer_Top.Add((self.barsize[0],0))
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Add(button,fill,wx.EXPAND)
                button.Show(True)
            self.sizer_Top.Add((10,10))
    
    def RemoveControls(self):
        """Removes all controls from the sizer"""
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Remove(button)
                
    def GetButton(self,section_id,button_id):
        """Gets a button object"""
        for active_section_id,section in self.sections.iteritems():
            if active_section_id == section_id:
                for active_button_id,button in section.buttons.iteritems():
                    if active_button_id == button_id:
                        return button
        return None # Not found
    
    def UnselectAllExcept(self,section_id,button_id):
        """Unselects all buttons except the one specified"""
        for active_section_id,section in self.sections.iteritems():
                for active_button_id,button in section.buttons.iteritems():
                    if not(active_button_id == button_id and active_section_id == section_id):
                        button.SetValue(False)
    
    def SelectButton(self,section_id,button_id):
        """Selects a button without deselecting anything"""
        button = self.GetButton(section_id,button_id)
        if button != None:
            button.SetValue(True)
            return True
        return False

    def Select(self,section_id,button_id):
        """Selects a button and deselects everything else, this doesn't raise an event"""
        button = self.GetButton(section_id,button_id)
        self.UnselectAllExcept(section_id,button_id)
        self.SelectButton(section_id,button_id)
        button.previous_button = self.currentbutton
        self.currentbutton = [section_id,button_id]
    
    def ToggleButton(self,section_id,button_id):
        """Checks if button is pressed, if it is NOT, select previous button"""
        button = self.GetButton(section_id,button_id)
        if button.GetValue():
            # Clicked a new button
            self.UnselectAllExcept(section_id,button_id)
            button.previous_button = self.currentbutton
            self.currentbutton = [section_id,button_id]
        else :
            # Clicked the current button
            if button.previous_button != None:
                if self.SelectButton(button.previous_button[0],button.previous_button[1]):
                    self.currentbutton = [button.previous_button[0],button.previous_button[1]]
                else:
                    # The previous button wasn't found
                    button.previous_button = None
                    button.SetValue(True)
            else:
                button.SetValue(True)

    def ButtonEvent(self,section_id,button_id):
        """Called whenever a button is clicked"""
        #print "Button event: section_id:",section_id," button_id:", button_id
        self.ToggleButton(section_id,button_id)
        if self.func_click is not None:
            self.func_click(self.currentbutton[0],self.currentbutton[1])

    def BindClick(self,func):
        """Bind a function to a Click event"""
        self.func_click = func

    def OnSize(self,event):
        """The Size event needs to be overloaded to hard-Refresh the buttons"""
        self.Layout()
        self.Refresh()
