# Circe
# Copyright (C) 2004 The Circe development team

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
        if(button_id in self.buttons):
            raise "Button %d already exists in section %d" % (button_id, self.section_id)
        else:
            self.buttons[button_id] = switchbutton(self.section_id,button_id,self.parent,text,icon)
            self.buttons[button_id].Show(False)
            # Bind event
            print "Binding with: ",self.buttons[button_id].event_id
            wx.EVT_BUTTON(self.parent,self.buttons[button_id].event_id,self.ButtonEvent)
    
    def RemoveButton(self,button_id):
        if(button_id in self.buttons):
            self.buttons[button_id].Destroy()
            del self.buttons[button_id]
        else:
            raise "Button %d does not exist in section %d" % (button_id, self.section_id)
    
    def RemoveAll(self):
        for button_id,button in self.buttons.iteritems():
            button.Destroy()
    
    def ButtonEvent(self,event):
        for button_id,button in self.buttons.iteritems():
            if(button.event_id == event.GetId()):
                # We found our event button
                self.parent.ButtonEvent(self.section_id,button.button_id)

class switchbutton(genbuttons.GenBitmapTextToggleButton):
    def __init__(self,section_id,button_id,parent,text,icon=None):
        self.button_id = button_id
        self.event_id = int(wx.NewId())
        self.text = text
        self.icon = icon
        self.parent = parent
        self.previous_button = None
        genbuttons.GenBitmapTextToggleButton.__init__(self,parent,self.event_id,icon,text)
        self.SetUseFocusIndicator(False)

class panel_switchbar(wx.Panel):
    def __init__(self,parent,panelID,barsize=-1,baralign=wx.HORIZONTAL):
        self.barsize = barsize
        self.baralign = baralign
        self.sections = {}
        self.currentbutton = None
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.barsize)
        
        self.CreateSizers()
        
        self.AddSection(0)
        self.AddButton(0,0,"Section 0 Button 0")
        self.AddButton(0,1,"Section 0 Button 1")
        self.AddButton(0,2,"Section 0 Button 2")
        self.AddSection(1)
        self.AddButton(1,0,"Section 1 Button 0")
        self.AddButton(1,1,"Section 1 Button 1")
        self.AddButton(1,2,"Section 1 Button 2")
        self.AddSection(2)
        self.AddButton(2,6,"Section 2 Button 6")
        self.AddButton(2,7,"Section 2 Button 7")
        self.AddButton(2,8,"Section 2 Button 8")
        #self.RemoveSection(1)
        #self.RemoveButton(2,4)
        self.AddControls()
    
    def Realize(self):
        self.RemoveControls()
        self.DestroySizers()
        self.CreateSizers()
        self.AddControls()
    
    def AddSection(self,section_id):
        if(section_id in self.sections):
            raise "Section %d already exists" % section_id
        else:
            self.sections[section_id] = switchsection(section_id,self)
    
    def RemoveSection(self,section_id):
        if(section_id in self.sections):
            self.sections[section_id].RemoveAll()
            del self.sections[section_id]
        else:
            raise "Section %d does not exist" % section_id
    
    def AddButton(self,section_id,button_id,text,icon=None):
        if(section_id in self.sections):
            self.sections[section_id].AddButton(button_id,text,icon)
        else:
            raise "Section %d does not exist" % section_id
    
    def RemoveButton(self,section_id,button_id):
        if(section_id in self.sections):
            self.sections[section_id].RemoveButton(button_id)
            del self.button_id_list[button_id]
        else:
            raise "Section %d does not exist" % section_id
    
    def SetAlignment(self,baralign,barsize):
        self.SetSize(barsize)
        self.baralign = baralign
        self.Realize()
    
    def DestroySizers(self):
        self.sizer_Top.Clear(False)
        self.sizer_Top.Destroy()
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(self.baralign)
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        fill = 0
        if (self.baralign == wx.HORIZONTAL):
            fill = 1
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Add(button,fill,wx.EXPAND)
                button.Show(True)
            self.sizer_Top.Add((10,10))
    
    def RemoveControls(self):
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Remove(button)
                
    def GetButton(self,section_id,button_id):
        for active_section_id,section in self.sections.iteritems():
            if(active_section_id == section_id):
                for active_button_id,button in section.buttons.iteritems():
                    if(active_button_id == button_id):
                        return button
        return None # Not found
    
    def UnselectAllExcept(self,section_id,button_id):
        for active_section_id,section in self.sections.iteritems():
                for active_button_id,button in section.buttons.iteritems():
                    if(not(active_button_id == button_id and active_section_id == section_id)):
                        button.SetValue(False)
    
    def SelectButton(self,section_id,button_id):
        # Selects a button
        button = self.GetButton(section_id,button_id)
        if(button != None):
            button.SetValue(True)
            return True
        return False
    
    def ToggleButton(self,section_id,button_id):
        # Checks if button is pressed, if it is NOT, select previous button
        button = self.GetButton(section_id,button_id)
        if(button.GetValue()):
            # Clicked a new button
            self.UnselectAllExcept(section_id,button_id)
            button.previous_button = self.currentbutton
            self.currentbutton = [section_id,button_id]
        else :
            # Clicked the current button
            if(button.previous_button != None):
                if(self.SelectButton(button.previous_button[0],button.previous_button[1])):
                    self.currentbutton = [button.previous_button[0],button.previous_button[1]]
                else:
                    # The previous button wasn't found
                    button.previous_button = None
                    button.SetValue(True)
            else:
                button.SetValue(True)

    def ButtonEvent(self,section_id,button_id):
        print "Button event: section_id:",section_id," button_id:", button_id
        self.ToggleButton(section_id,button_id)
