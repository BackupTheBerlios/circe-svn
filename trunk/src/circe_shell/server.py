import ircclient
import ircreactor

class Server:
    def __init__(self,host=None,port=None):
        self.channels = None
        self.host = host
        self.port = port
        self.factory = ircclient.ClientFactory()
        if(self.host != None):
            self.Connect(host,port)

    def Connect(self,host,port=6667):
        """Connects to a given server"""
        #Todo: get default port
        self.host = host
        self.port = port
        print "Connecting to:",host,port
        ircreactor.reactor.connectTCP(host,port,self.factory)

    def Join(self,channelname):
        """Joins a channel on this server and returns a channel object"""
        pass
