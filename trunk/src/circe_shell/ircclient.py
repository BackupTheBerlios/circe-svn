from twisted.protocols import irc
from twisted.internet import protocol

class Client(irc.IRCClient):
    """The gateway between the abstracted classes and irc.IRCClient"""
    def __init__(self,server):
        #self.nickname = "circe_test"
        self.server = server
        # Call the server object to announce myself
        server.InitClient(self)

    # Connection events
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.server.ConnectionMade()

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.server.ConnectionLost(reason)

    # IRC events
    def signedOn(self):
        self.server.SignedOn()

    def joined(self,channel):
        self.server.Joined(channel)

class ClientFactory(protocol.ClientFactory):
    """A factory for clients."""
    def __init__(self,server):
        self.protocol = Client
        self.server = server

    def clientConnectionLost(self, connector, reason):
        print "Connection lost:", reason

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:", reason

    def buildProtocol(self,addr):
        """Builds the protocol, with custom __init__"""
        p = self.protocol(self.server)
        p.factory = self
        return p
