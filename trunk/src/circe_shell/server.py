import ircclient
import ircreactor

class Server:
    def __init__(self,host=None,port=None):
        self.channels = None
        self.host = host
        self.port = port
        self.factory = ircclient.ClientFactory(self)
        if(self.host != None):
            self.Connect(host,port)

    def Connect(self,host,port=6667):
        """Connects to a given server"""
        #Todo: get default port
        self.host = host
        self.port = port
        print "Connecting to:",host,port
        c = ircreactor.reactor.connectTCP(host,port,self.factory)

    def Join(self,channelname):
        """Joins a channel on this server and returns a channel object"""
        self.client.join(channelname)

    # Events
    def OnInit(self,client):
        """Sets the client object used by this server"""
        self.client = client
        
    def ConnectionMade(self):
        print "Connected!"

    def ConnectionLost(self,reason):
        print "Connection lost!"

    def SignedOn(self):
        print "Signed on!"
        self.Join("#circe")
