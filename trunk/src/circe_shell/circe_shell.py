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