class maskcontainer:
    def __init__(self,maskstring = None):
        self.username = ""
        self.address = ""
        if(modestring != None):
            setmodestring(modestring)
        
    def getusername(self):
        return self.username
    def setusername(self,username):
        self.username = username
        
    def getaddress(self):
        return self.address
    def setaddress(self,address):
        self.address = address
        
    def getmaskstring(self):
        pass
    
    def setmaskstring(self,maskstring):
        pass