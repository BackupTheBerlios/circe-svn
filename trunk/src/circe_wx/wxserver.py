from window_status import window_status
from window_channel import window_channel
from circelib.circelib import Server

class WXServer(Server):
    def __init__(self,windowarea,host=None,port=None):
        Server.__init__(self,host,port)
        self.statuswindow = window_status(windowarea,self)
        windowarea.AddWindow(self.statuswindow)
        self.windowarea = windowarea
        self.channels = []

    def NewChannelWindow(self,channelname):
        new = window_channel(self.windowarea,self,channelname)
        self.windowarea.AddWindow(new)
        self.channels.append(new)

    def TextCommand(self,cmdstring,window):
        if cmdstring == None or len(cmdstring) == 0:
            raise "Empty command"
        # Strip /
        if cmdstring[0] == "/":
            cmdstring = cmdstring[1:]
        else:
            return
        # Create a list
        cmdlist = cmdstring.split()
        cmd = cmdlist[0]
        params = cmdlist[1:]
        # Find out what command is being executed
        if cmd == "server":
            self.connect(*params)
        elif cmd == "join":
            self.joinChannel(*params)
        elif cmd == "nick":
            self.nick(*params)
        elif cmd == "msg":
            channel = params[0]
            text = params[1:]
            text=" ".join(text)
            self.sendMessage(channel, text)
        elif cmd == "quit":
            self.closeConnection()
        # For debug purposes:
        elif cmd == "joindebug":
            self.NewChannelWindow(params[0])
