from window_status import window_status
from window_channel import window_channel
from circelib.circelib import CirceIRCClient


class WXServer(CirceIRCClient):
    def __init__(self,windowarea, target=""):
        CirceIRCClient.__init__(self, target)
        self.host = self.target
        self.statuswindow = window_status(windowarea,self)
        windowarea.AddWindow(self.statuswindow)
        self.windowarea = windowarea
        self.channels = []

    def NewChannelWindow(self,channelname):
        new = window_channel(self.windowarea,self,channelname)
        self.windowarea.AddWindow(new)
        self.channels.append(new)

    def TextCommand(self,cmdstring,window):
        if not cmdstring:
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
            # /server servername nickname
            server = params[0]
            port = 6667
            nick = params[1]
            self.connection.connect(server=server, port=port, nickname=nick)
        elif cmd == "join":
            self.connection.join(*params)
        elif cmd == "nick":
            self.connection.nick(*params)
        elif cmd in ("msg", "privmsg"):
            channel = params[0]
            text = params[1:]
            text=" ".join(text)
            self.connection.privmsg(channel, text)
        elif cmd == "quit":
            self.connection.disconnect()
        elif cmd == "joindebug":
            self.NewChannelWindow(params[0])
