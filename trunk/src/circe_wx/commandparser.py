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

from window_channel import window_channel

def NewChannelWindow(windowarea,id,server):
    newchannel = window_channel(windowarea,id,server)
    windowarea.AddWindow(newchannel)
    return newchannel

def TextCommand(server,windowarea,cmdstring):
    if(cmdstring == None or len(cmdstring) == 0):
        raise "Empty command"
    # Strip /
    if cmdstring[0] == "/":
        cmdstring = cmdstring[1:]
    else:
        return
    # Create a list
    cmdlist = cmdstring.split()
    cmd = cmdlist[0]
    params = cmdlist[1:]
    # Find out what command is being executed
    if(cmd == "server"):
        server.connect(*params)
    elif(cmd == "join"):
        server.joinChannel(*params)
    elif(cmd == "nick"):
        server.nick(*params)
    elif(cmd == "msg"):
        channel = params[0]
        text = params[1:]
        text=" ".join(text)
        server.sendMessage(channel, text)
    elif(cmd == "quit"):
        server.closeConnection()
    # For debug purposes:
    elif(cmd == "joindebug"):
        NewChannelWindow(windowarea,-1,server)
