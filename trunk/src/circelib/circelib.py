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

import socket, circe_globals
class Server:
    def __init__(self, host=None, port=None):
        global IC
        IC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        if(host != None):
            self.connect(host,port)
    def connect(self, host, port=6667):
        self.host = host
        self.port = port
        IC.connect((host,int(port)))
    def nick(self, nick, user="circe", host="circe"):
        IC.send("USER %s %s %s %s\r\n" % (nick, user,host,user))
        IC.send("NICK %s %s\r\n" % (nick, user))
    def send(self, ts):
        IC.send("%s\r\n" % (ts))
    def nickChange(self, newnick):
        IC.send("NICK %s\r\n" % (newnick))
    def joinChannel(self, channel, channelpass=""):
        IC.send("JOIN %s %s\r\n" % (channel, channelpass))
    def partChannel(self, channel, partmessage):
        IC.send("PART %s %s\r\n" % (channel, partmessage))
    def sendMessage(self, channel, message):
        IC.send("PRIVMSG %s :%s\r\n" % (str(channel), str(message)))
    def closeConnection(self):
        quitmsg = circe_globals.QUITMSG
        IC.send("QUIT %s\r\n" % (str(quitmsg)))
        IC.close()
    def sendAction(self, channel, action):
        IC.send("PRIVMSG %s :\001ACTION %s\001" % (channel, action))
    def sendMode(self, channel, mode, args):
        IC.send("MODE %s %s %s" % (channel, mode, args))
    def sendKick(self, channel, person, reason):
        IC.send("KICK %s %s %s" % (channel, person, reason))
    def chanTopic(self, channel, nt):
        IC.send("TOPIC %s %s" % (channel, nt))
