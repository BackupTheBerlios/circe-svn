from window_status import window_status
from window_channel import window_channel
import irclib


class CirceIRCClient(irclib.SimpleIRCClient):
    """Simple IRC client inspired from SimpleIRCClient from python-irclib."""
    def __init__(self):
        self.ircobj = irclib.IRC()
        self.connection = self.ircobj.server()
        self.ircobj.add_global_handler("all_events", self._processEvents)
        # Here are stored Events objects to be processed (use Event's methods
        # eventtype(), source(), target(), arguments() to have all info about
        # the event)
        self.new_events = []

    def _processEvents(self, c, e):
        """Add events to self.new_events."""
        self.new_events.append(e)

    def connect(self, server, port, nickname, password=None, username=None,
            ircname=None, localaddress="", localport=0):
        """Connect/reconnect to a server."""
        self.connection.connect(server, port, nickname, password, username,
                ircname, localaddress, localport)

    def setDebug(self, flag):
        """Turn on/off the debug mode."""
        irclib.DEBUG = flag
        print "Debug mode", flag and "on" or "off"

    def checkEvents(self):
        """Check for new events, then return them in a list or return an empty
        list if there is no new event.
        """
        self.new_events = []
        self.ircobj.process_once()
        return self.new_events

    
class WXServer(CirceIRCClient):
    def __init__(self,windowarea):
        CirceIRCClient.__init__(self)
        self.c = self.connection    # just because it's shorter
        self.host = self.c.connected and self.c.get_server_name() or ""
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
            self.host = server
            # XXX TEST
            print "Server: %s %s" % (server,
                    self.connection.get_server_name())
        elif cmd =="check": # for testing
            print "-"*10, "CheckEvents"
            for e in self.checkEvents():
                print "--\nEvent: %s Source: %s Target: %s\nArguments: %s" % ( 
                        e.eventtype(), e.source(), e.target(), e.arguments())
        elif cmd == "debug":
            self.setDebug(True)
        elif cmd == "nodebug":
            self.setDebug(False)
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
