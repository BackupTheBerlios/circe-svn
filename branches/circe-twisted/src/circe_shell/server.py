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

import ircclient
import ircreactor

class Server:
    def __init__(self,host=None,port=None):
        """The Server class, interfaces between the UI and the IRC code"""
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
        ircreactor.reactor.connectTCP(host,port,self.factory)
    
    def InitClient(self,client):
        """Sets the client object used by this server"""
        self.client = client

    # IRC methods
    def Join(self,channelname):
        """Joins a channel on this server and returns a channel object"""
        channelname = str(channelname)
        self.client.join(channelname)

    def Say(self,channel,text,length=None):
        """Says into a channel"""
        channel = str(channel)
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
