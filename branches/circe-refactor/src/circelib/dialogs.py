import wx

class NicknameAskDialog(wx.TextEntryDialog):
    """a wx.TextEntryDialog that shows itself until:
       * the user has given a value OR
       * if ntimes is specified AND is not 0, the user hasn't typed anything in (or presses cancel) n times
    """
    def __init__(self, parent, ntimes=None):
        wx.TextEntryDialog.__init__(self, parent, "Please choose a nickname:")
        self.ntimes = ntimes or 0
        self.count = 0
    def GetValue(self):
        result = ''
        while result == '': # while user has typed in a blank string and pressed ok (or just pressed cancel)
            result = wx.TextEntryDialog.GetValue(self) # upcall to do the actual work
            if result: # 
                self.Destroy()
                return result
            self.Show()

            if self.ntimes == 0:
                continue # infinite
            elif self.ntimes < self.count:
                self.ntimes += 1
            elif self.ntimes == self.count:
                self.Destroy()
                return ''
        return result
