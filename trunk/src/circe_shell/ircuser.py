from maskcontainer import maskcontainer

class ircuser:
    def __init__(self,server,username):
        self.server = server
        self.username = username
        self.fullname = ""
        self.mask = maskcontainer()

    def getname(self):
        return self.username
    
    def getfullname(self):
        return self.fullname
    
    def getmask(self):
        return self.mask