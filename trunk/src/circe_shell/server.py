import ircclient
import ircreactor

class Server:
    def __init__(self,host=None,port=None):
        """The Server class, interfaces between de UI and the IRC code"""
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
        ircreactor.reactor.connectTCP(host,port,self.factory)
    
    def InitClient(self,client):
        """Sets the client object used by this server"""
        self.client = client

    # IRC methods
    def Join(self,channelname):
        """Joins a channel on this server and returns a channel object"""
        self.client.join(channelname)

    def Say(self,channel,text,length=None):
        """Says into a channel"""
        self.client.say(channel,text,length)

    # Events
    def ConnectionMade(self):
        pass

    def ConnectionLost(self,reason):
        pass

    def SignedOn(self):
        pass

    def Joined(self,channel):
        pass
