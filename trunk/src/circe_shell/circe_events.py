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

class circe_events:
	""" I hold all overridable events. """
	
	# Todo DCC Events:
	# Chat DccServer FileRcvd FileSent GetFail SendFail Serv
	
	def e_Action(self):
		pass
	def e_Ban(self):
		pass
	def e_Chat(self):
		pass
	def e_Connect(self):
		pass
	def e_Ctcp(self):
		pass
	def e_CtcpReply(self):
		pass
	def e_DeHelp(self):
		pass
	def e_DeOp(self):
		pass
	def e_DeVoice(self):
		pass
	def e_Dns(self):
		pass
	def e_Error(self):
		pass
	def e_Exit(self):
		pass
	def e_Invite(self):
		pass
	def e_Join(self):
		pass
	def e_Kick(self):
		pass
	def e_Logon(self):
		pass
	def e_Mode(self):
		pass
	def e_Nick(self):
		pass
	def e_Notice(self):
		pass
	def e_Notify(self):
		pass
	def e_Op(self):
		pass
	def e_Part(self):
		pass
	def e_Ping(self):
		pass
	def e_Pong(self):
		pass
	def e_Quit(self):
		pass
	def e_Raw(self):
		pass
	def e_ServerMode(self):
		pass
	def e_ServerOp(self):
		pass
	def e_Snotice(self):
		pass
	def e_Text(self):
		pass
	def e_Topic(self):
		pass
	def e_Unban(self):
		pass
	def e_Unotify(self):
		pass
	def e_UserMode(self):
		pass
	def e_Voice(self):
		pass
	def e_Wallops(self):
		pass