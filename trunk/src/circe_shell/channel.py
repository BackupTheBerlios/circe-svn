from modecontainer import modecontainer

class channel:
    def __init__(self,server,channelname):
        self.server = server
        self.channelname = channelname
        self.topic = ""
        self.joined = False
        self.modes = modecontainer()
        self.users = []
    
    def join(self,cname = self.channelname):
        pass
    
    def part(self)
        pass
    
    def rejoin(self):
        self.part()
        self.join()
    
    def setchannel(self,cname)
        if(!self.joined):
            self.channelname = cname
    
    def getchannel(self):
        return self.channelname