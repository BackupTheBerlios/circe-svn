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
        
        self.CreateControls()
        self.CreateSizers()
        self.AddControls()
        
        self.AddSection(0)
        self.AddButton(0,0,"Section 0 Button 0")
        self.AddButton(0,1,"Section 0 Button 1")
        self.AddSection(1)
        self.AddButton(1,0,"Section 1 Button 0")
        self.AddButton(1,1,"Section 1 Button 1")
        self.RefreshButtons()
    
    def RefreshButtons(self):
        self.RemoveControls()
        self.AddControls()
    
    def AddSection(self,section_id):
        if(section_id in self.sections):
            raise "Section %d already exists" % section_id
        else:
            self.sections[section_id] = switchsection(section_id)
    
    def AddButton(self,section_id,button_id,text,icon=None):
        if(section_id in self.sections):
            self.sections[section_id].AddButton(button_id,self,text,icon)
        else:
            raise "Section %d does not exist" % section_id
    
    def SetAlignment(self,baralign,barsize):
        self.SetSize(barsize)
        self.baralign = baralign
        self.RemoveControls()
        self.DestroySizers()
        self.CreateSizers()
        self.AddControls()
        
    def CreateControls(self):
        pass
    
    def DestroySizers(self):
        del self.sizer_Top
    
    def CreateSizers(self):
        self.sizer_Top = wx.BoxSizer(self.baralign)
        self.SetSizer(self.sizer_Top)
    
    def AddControls(self):
        #self.sizer_Top.Add(self.switchbar,1,wx.EXPAND)
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                print "Add button: %s" % button.text
                self.sizer_Top.Add(button,0,wx.EXPAND)
            print "Add 10!"
            self.sizer_Top.Add((10,10))
    
    def RemoveControls(self):
        for section_id,section in self.sections.iteritems():
            for button_id,button in section.buttons.iteritems():
                self.sizer_Top.Remove(button)