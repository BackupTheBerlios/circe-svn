from maskcontainer import maskcontainer

class ircuser:
    def __init__(self,server,username):
        self.server = server
        self.username = username
        self.fullname = None
        self.host = None
        self.mask = maskcontainer()

    def getname(self):
        return self.username
    
    def getfullname(self):
        return self.fullname
    
    def gethost(self):
        return self.host
    
    def getmask(self):
        return self.mask