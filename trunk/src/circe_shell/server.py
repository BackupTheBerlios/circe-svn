class server:
    def __init__(self):
        self.connected = False
        self.servername = None # Servername will be specified by the server
        self.network = None
        self.address = None
        self.channels = []
    
    def connect(self,caddr = self.address):
        pass
    
    def disconnect(self)
        pass
    
    def reconnect(self):
        self.disconnect()
        self.connect()
    
    def setaddress(self,caddr)
        if(!self.connected):
            self.address = caddr
    
    def getaddress(self):
        return self.address
    
    def getname(self):
        return self.servername