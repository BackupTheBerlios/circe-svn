from twisted.protocols import irc
from twisted.internet import protocol

class Client(irc.IRCClient):
    """The gateway between the server object and irc.IRCClient"""
    
    def __init__(self):
        self.nickname = "circe_test"

    def connectionMade(self):
        print "Connected!"
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        print "Connection lost!"
        irc.IRCClient.connectionLost(self, reason)

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        pass

class ClientFactory(protocol.ClientFactory):
    """A factory for clients."""

    # the class of the protocol to build when new connection is made
    protocol = Client

    def __init__(self):
        pass

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        print "Connection lost:", reason

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed:", reason
