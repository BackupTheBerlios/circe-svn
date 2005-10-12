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

class ircusers:
	def __init__(self):
		self.users = {}
	def getUser(self,nickname):
		if self.users.has(nickname):
			return self.users[nickname]
		else:
			return None
			
	def addUser(self,nickname):
		if self.users.has(nickname):
			self.users[nickname].update(nickname)
		else:
			self.users[nickname].add(nickname)
			
	def delUser(self,nickname):
		if self.users.has(nickname):
			del(self.users[nickname])

class ircuser:
	""" ircuser is an object containing information about an irc user. """
	def __init__(self,server,nickname,username=None,hostname=None,fullname=None):
		self.server = server
		self.nickname = nickname
		self.username = username
		self.fullname = fullname
		self.hostname = hostname
		self.mask = maskcontainer(self)
		
	def getnick(self):
		""" returns nickname """
		return self.nickname
	def getfullname(self):
		""" returns full name if available, None if not. """
		return self.fullname
	def getusername(self):
		""" returns username (ident) if available, None if not. """
		return self.username
	def gethost(self):
		""" returns hostname if available, None if not. """
		return self.mask.getmaskbystring("$h")
	def gethostmask(self):
		""" returns the hostmask container object. """
		return self.mask

class maskcontainer:
    def __init__(self,parent):
        """\
for now, parent.nickname,username,hostname is used.
splitting it up would be stupid. """
	## following are used
	# parent.username
	# parent.nickname
	# parent.hostname
        def getobscuremask(self):
            pass
        def gethostmask(self):
            """ *!*@domain.com """
            return self.getmaskbystring("*!*@$h")
            
	def getnickmask(self):
            """ nickname!*@* """
		return self.getmaskbystring("$n!*@*")
	def getusermask(self):
            """ *!~ident@* """
		return self.getmaskbystring("*!$u@*")
	def getdomainmask(self):
            """ *!*@domain.* """
		return self.getmaskbystring("*!*@$d.*")
	def getbestmask(self):
            """\
For scripting purposes, if you are unsure about what host information that are
available, this is the best option, as it will select the most specific hostmask.
If you need a complete list, your script should do a /who #channel to update the
ircuser objects with complete host information."""

            if parent.hostname != None: #BEST
                return self.gethostmask()

            if ((parent.username != None) and (parent.hostname == None)):
                # I dont see how this could ever happen... but its still
                # possible to give a good hostmask :)
                return self.getusermask()

            if ((parent.hostname == None) and (parent.username == None)):
                return self.getnickmask()

            raise "Omg, this function is screwed! No data to make mask from!\nMail nookie@online.no and tell me I need my head examined!"	

	def getmaskbystring(self,maskstring):
	"""\
This function returns a hostmask in desired format.
Example: $n!$u@$d.$t -> nickname!username@domain.org
$n is nickname
$u is username (ident)
$h is hostname (This is equal to $d.$t)
$d is domain (domain.xxx)
$t is toplevel domain (org/net/com).
Remeber: the $'s are case sensitive. """
	output = maskstring
	if parent.hostname == None:
		hostname = "*"
		topdomain = "*"
		domain = "*"
	else:
		hostname = parent.hostname
		topdomain = string.split(host,".")[-1:]
		domain = string.join(string.split(host,".")[:-1],".")

	output = string.replace(maskstring,"$n",parent.nickname)
	output = string.replace(maskstring,"$u",parent.username)
	output = string.replace(maskstring,"$h",hostname)
	output = string.replace(maskstring,"$d",domain)
	output = string.replace(maskstring,"$t",topdomain)

	return output
