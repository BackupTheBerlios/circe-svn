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

from circe_network import circe_network
from circe_events import circe_events
from circe_actions import circe_actions
from twisted.basic import reactor

class circe_shell(circe_network):
	pass

                
if __name__ == "__main__":
    print "running test.."
    from circe_network import circe_network_factory
    reactor.connectTCP("irc.freenode.org",6667,circe_network_factory())
    reactor.run()
