import server
import ircreactor

class testserver(server.Server):
    def __init__(self):
        server.Server.__init__(self)
        
    def ConnectionMade(self):
        print "Connected!"
        
    def SignedOn(self):
        print "Signed on!"        
        self.Join("#circe")

    def Joined(self,channel):
        print "Joined %s!" % channel
        self.Say(channel,"Hello world!")

t = testserver()
t.Connect("localhost")

ircreactor.Run()
