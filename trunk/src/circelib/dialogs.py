import wx
class AskNicknameDialog(wx.TextEntryDialog):
    def __init__(self, *args, **kwargs):
        self.in_use = kwargs.get("in_use")
        try:
            self.times = args[1]
        except IndexError:
            self.times = 2
        if self.in_use:
            return super(AskNicknameDialog, self).__init__(None, "Nickname (%s) is in use. Please select a different one:" % args[0])
        else:
            return super(AskNicknameDialog, self).__init__(None, "Please select a nickname:")

    def GetValue(self, times=0):
        self.Hide()
        result = super(AskNicknameDialog, self).GetValue()
        if times < self.times and not result:
            self.ShowModal()
            return self.GetValue(times+1)
        else:
            if result:
                return result
            else:
                return ""

        if not self.in_use:
            return result
        elif result == self.nickname:
            self.ShowModal()
            return self.GetValue()
        else:
            return result

def ask_nickname(nickname=None, times=2):
    if nickname:
        ask_nickname = AskNicknameDialog(nickname, times, in_use=1)
    else:
        ask_nickname = AskNicknameDialog()
    ask_nickname.ShowModal()
    return ask_nickname.GetValue()
