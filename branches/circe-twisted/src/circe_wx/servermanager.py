from circe_shell.server import Server

servers = []

class WXServer(Server):
    """This class catches all the events from the Server object"""
    def __init__(self,*options):
        Server.__init__(self,*options)
        self.statuswindow = None
        self.channels = None

    def SetStatusWindow(self,statuswindow):
        self.statuswindow = statuswindow
        
    def AddChannel(self,channel):
        pass

    def RemoveChannel(self,channel):
        pass

    def ConnectionMade(self):
        self.statuswindow.ServerEvent("Connected to %s:%s" % (self.host,self.port))

    def ConnectionLost(self,reason):
        self.statuswindow.ServerEvent("Connection to %s lost, reason: %s" % (self.host,reason))

    def SignedOn(self):
        self.statuswindow.ServerEvent("Signed on to %s" % self.host)

    def Joined(self,channel):
        self.statuswindow.ServerEvent("Joined %s" % channel)
        
def AddServer(*options):
    s = WXServer(*options)
    servers.append(s)
    return s

def RemoveServer(s):
    if s in servers:
        del servers[s]

def TextCommand(server,cmdstring):
    if(cmdstring == None or len(cmdstring) == 0):
        raise "Empty command"
    # Strip /
    if cmdstring[0] == "/":
        cmdstring = cmdstring[1:]
    # Create a list
    cmdlist = cmdstring.split()
    cmd = cmdlist[0]
    params = cmdlist[1:]
    if(cmd == "server"):
        server.Connect(*params)
    elif(cmd == "join"):
        server.Join(*params)
