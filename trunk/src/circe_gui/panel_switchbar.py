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
    def __init__(self,section_id):
        self.section_id = section_id
        self.buttons = {}
    
    def AddButton(self,button_id,parent,text,icon=None):
        if(button_id in self.buttons):
            raise "Button %d already exists in section %d" % (button_id, self.section_id)
        else:
            self.buttons[button_id] = switchbutton(button_id,parent,text,icon)
            self.buttons[button_id].Show(False)
    
    def RemoveButton(self,button_id):
        if(button_id in self.buttons):
            self.buttons[button_id].Destroy()
            del self.buttons[button_id]
        else:
            raise "Button %d does not exist in section %d" % (button_id, self.section_id)
    
    def RemoveAll(self):
        for button_id,button in self.buttons.iteritems():
            button.Destroy()

class switchbutton(genbuttons.GenBitmapTextToggleButton):
    def __init__(self,button_id,parent,text,icon=None):
        self.button_id = button_id
        self.text = text
        self.icon = icon
        genbuttons.GenBitmapTextToggleButton.__init__(self,parent,button_id,icon,text)
        self.SetUseFocusIndicator(False)

class panel_switchbar(wx.Panel):
    def __init__(self,parent,panelID,barsize=-1,baralign=wx.HORIZONTAL):
        self.barsize = barsize
        self.baralign = baralign
        self.sections = {}
        wx.Panel.__init__(self,parent,panelID,wx.DefaultPosition,self.barsize)
        
        self.CreateSizers()
        
        self.AddSection(0)
        self.AddButton(0,0,"Section 0 Button 0")
        self.AddButton(0,1,"Section 0 Button 1")
        self.AddSection(1)
        self.AddButton(1,2,"Section 1 Button 2")
        self.AddButton(1,3,"Section 1 Button 3")
        self.AddSection(2)
        self.AddButton(2,4,"Section 2 Button 4")
        self.AddButton(2,5,"Section 2 Button 5")
        self.RemoveSection(1)
        self.RemoveButton(2,4)
        self.Realize()
    
    def Realize(self):
        self.RemoveControls()
        self.DestroySizers()
        self.CreateSizers()
        self.AddControls()
    
    def AddSection(self,section_id):
        if(section_id in self.sections):
            raise "Section %d already exists" % section_id
        else:
            self.sections[section_id] = switchsection(section_id)
    
    def RemoveSection(self,section_id):
        if(section_id in self.sections):
            self.sections[section_id].RemoveAll()
            del self.sections[section_id]
        else:
            raise "Section %d does not exist" % section_id
    
    def AddButton(self,section_id,button_id,text,icon=None):
        if(section_id in self.sections):
            self.sections[section_id].AddButton(button_id,self,text,icon)
        else:
            raise "Section %d does not exist" % section_id
    
    def RemoveButton(self,section_id,button_id):
        if(section_id in self.sections):
            self.sections[section_id].RemoveButton(button_id)
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
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Add(button,0,wx.EXPAND)
                button.Show(True)
            self.sizer_Top.Add((10,10))
    
    def RemoveControls(self):
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Remove(button)