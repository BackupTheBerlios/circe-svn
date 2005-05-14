# Circe
# Copyright (C) 2004-2005 The Circe development team

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

import irclib



class Server:
    """IRC client inspired from SimpleIRCClient from python-irclib.
    It can handles several connections to multiple servers.
    """

# XXX To uncomment if patch 1197200 at sourceforge is applied to python-irclib. And 
# XXX remove the other initialization above.
#
#    ircobj = irclib.IRC()
#

    def __init__(self, target):
        """Arguments:
            target -- a nick or a channel name
        """
        self._debug = False
        self.ircobj = irclib.IRC()
        self.connection = self.ircobj.server()
        self.ircobj.add_global_handler("all_events", self._storeEvents)
        self._target = target
        # Here are stored Events objects to be processed (use Event's methods
        # eventtype(), source(), target(), arguments() to get all info about
        # events)
        self._events = []

    def _storeEvents(self, c, e):
        """Adds events to self.new_events."""
        self._events.append(e)

    def connect(self, server, port, nickname, password=None, username=None,
            ircname=None, localaddress="", localport=0):
        """Connects/reconnects to a server."""
        self.connection.connect(server, port, nickname, password, username,
                ircname, localaddress, localport)

    def getConnection(self):
        return self.connection

    def setDebug(self):
        """Turns on the debug mode."""
        self._debug = True
        irclib.DEBUG = True
        print "Debug mode on"

    def noDebug(self):
        """Turns off the debug mode."""
        self._debug = False
        irclib.DEBUG = False
        print "Debug mode off"

    def getEvents(self):
        """Gets new events, stores them in self._events and returns them in a
        list if there are some new ones.
        """
        self._events = []
        self.ircobj.process_once(timeout=0.1)
        return self._events

