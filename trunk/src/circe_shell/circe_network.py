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

import string

	

class circe_network(circe_events,circe_actions):

    def connectionMade(self):
            irc.IRCClient.connectionMade(self)
            e_Connect()
            
            # Get my own object here!!!
    
    # Joins and parts   
	def joined(self, channel):		
		e_Join(self.ircusers.myself(), channel)
		
	def userJoined(self,user,channel):
		# Concidered broke, user is only nickname, not complete mask!
		
		# What to do here:
		# run ircusers.update(user), which splits the string correctly.
		#ircusers.update( ircuser(nickname,...) )
	
	def parted(self, channel):
		e_Part(self.ircusers.myself(), channel)
	
	def userParted(self,user,channel):
		e_Part(self,ircusersobj,channelobj)
	
	###
	
	
		
    def modeChanged(self,user, channel, set, modes, args):
        self.msg(channel,"I saw you %s change modes!" % user)
    def topicUpdated(self,user, channel, newTopic):
        if not user == "ChanServ":
            self.msg(channel,"But I liked the old topic, %s" % user)
    def userKicked(self, kickee, channel, kicker, message):
        self.msg(channel,"Please dont kick me as well %s" % kicker)
    def userRenamed(self, oldname, newname):
        self.msg(newname,"I liked your old nickname %s much better" % oldname)
    def privmsg(self,user,channel,message):
        print user
        print channel
        print message
        if string.upper(string.split(message)[0]) == "JOIN":
            print "join order"
            self.join(string.split(message)[1])
        if string.upper(string.split(message)[0]) == "PART":
            print "part order"
            self.part(string.split(message)[1])
        if string.upper(string.split(message)[0]) == "MSG":
            print "message order"
            self.msg(string.split(message)[1],string.join(string.split(message)[2:]," "))
        if string.upper(string.split(message)[0]) == "TERMINATE":
            print "terminate order"
            reactor.stop()
    def userJoined(self,user,channel):
        if string.lower(channel) == "#circe":
            if string.lower(user) == "anjel":
                self.msg(user,"Hi, im Noen's first network code of circle_shell. Remote commands are: MSG <target> <message>, JOIN <channel>, PART <channel>.")
                
