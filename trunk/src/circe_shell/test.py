import server
import ircreactor

print "Connecting to infi..."
newserver = server.Server()
newserver.Connect("irc.freenode.net")

ircreactor.Run()
