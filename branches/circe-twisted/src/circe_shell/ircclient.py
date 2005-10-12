# Circe
# Copyright (C) 2004 The Circe development team

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

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
