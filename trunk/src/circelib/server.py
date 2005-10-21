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

import circeirc as irclib



class Server:
    """IRC client inspired from SimpleIRCClient from python-irclib.
    It can handles several connections to multiple servers.
    """

    def __init__(self):

        """Arguments: None"""
        self.debug = False
        self.ircobj = irclib.IRC()
        self.ircobj.add_global_handler("all_events", self._store_events)
        self.connection = self.ircobj.server()
        # Here are stored Events objects to be processed (use Event's methods
        # eventtype(), source(), target(), arguments() to get all info about
        # events)
        self._events = []

    def _store_events(self, c, e):
        """Add events to self.new_events."""
        self._events.append(e)


    def connect(self, cmd, window, **kwargs):
        """Connect/reconnect to a server."""
        kwargs['server']
        try:
            kwargs['port']
            try: 
                int(kwargs['port'])
            except ValueError:
                raise KeyError
        except KeyError:
            kwargs['port'] = 6667
        try:
            kwargs['nickname']
        except KeyError:
            kwargs['nickname'] = "circe"
        self.connection.connect(**kwargs)

    def setdebug(self, boolean):
        """Turn on/off the debug mode depending on the value of 'boolean'."""
        self.debug = boolean
        irclib.DEBUG = boolean
        toggle = ["on", "off"]
        map = {True: 0, False: 1}
        msg = "Debug mode %s"
        integer  = map[boolean]
        string = toggle[integer]
        msg = msg % string
        print msg

    def get_events(self):
        """Get new events, store them in self._events and return them in a
        list if there are some new ones.
        """
        self._events = []
        self.ircobj.process_once(timeout=0.1)
        return self._events

