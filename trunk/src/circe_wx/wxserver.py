from window_status import window_status
from window_channel import window_channel
import irclib


class CirceIRCClient:
    """Simple IRC client inspired from SimpleIRCClient from python-irclib."""
    def __init__(self, target):
        """Arguments:
            target -- a nick or a channel name
        """
        # DEBUGGING
        irclib.DEBUG = True
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

    def setDebug(self, flag):
        """Turns on/off the debug mode."""
        irclib.DEBUG = flag
        print "Debug mode", flag and "on" or "off"

    def getEvents(self):
        """Gets new events, stores them in self._events and returns them in a
        list if there are some new ones.
        """
        self._events = []
        self.ircobj.process_once(timeout=0.1)
        return self._events


class WXServer(CirceIRCClient):
    def __init__(self,windowarea):
        CirceIRCClient.__init__(self, target="")
        c = self.connection
        self.host = c.connected and c.get_server_name() or None
        self.statuswindow = window_status(windowarea,self)
        windowarea.AddWindow(self.statuswindow)
        self.windowarea = windowarea
        self.channels = []

    def getHostname(self):
        """Returns the host we are connected to."""
        return self.host

    def is_connected(self):
        return self.connection.is_connected()

    def NewChannelWindow(self,channelname):
        """Opens a new channel window, sets the caption and stores it."""
        if self.connection.connected:
            nick = self.connection.get_nickname()
        else:   # for debug window
            nick = "not connected"
        caption = "%s(%s)" % (channelname, nick)
        new = window_channel(self.windowarea,self,channelname)
        new.SetCaption(caption)
        self.windowarea.AddWindow(new)
        self.channels.append(new)
        return new

    def getWindowChannelRef(self, channelname):
        """Returns the window_channel object binded to channelname or False if
        it does not match.
        """
        for window in self.channels:
            if window.getChannelname() == channelname:
                return window
        return False

    def TextCommand(self,cmdstring,window):
        if not cmdstring:
            raise "Empty command"

        # in a debug window, do nothing
        if hasattr(window, "getChannelname") and \
            window.getChannelname() == "Debug window":
#            window.setUsers(["hello", "test"])
            return

        # Strip /
        if cmdstring[0] == "/":
            cmdstring = cmdstring[1:]
        else:
            # if it is not a command send the message to the channel
            if hasattr(window, "getChannelname"):
                target = window.getChannelname()
                self.connection.privmsg(target, cmdstring)
                mynick = self.connection.get_nickname()
                window.addMessage(cmdstring, mynick)
            return
        # Create a list
        cmdlist = cmdstring.split()
        cmd = cmdlist.pop(0)
        params = cmdlist

        # Find out what command is being executed
        if cmd == "server":
            # /server servername nickname
            if len(params) < 1:
                raise TypeError, "You should supply two arguments: servername\
                                    and nick"
            server, nick = params
            port = 6667
            self.connect(server=server, port=port, nickname=nick)
            self.host = server
            # Check regularly for new events
            self.statuswindow.enableChecking()

        elif cmd == "action":
            self.connection.action(target=params[0], action=params[1])
        elif cmd == "globops":
            self.connection.globops(params[0])
        elif cmd == "info":
            self.connection.info(*params)   # optional arg: server
        elif cmd == "invite":
            self.connection.invite(nick=params[0], channel=params[1])
        elif cmd == "ison":
            self.connection.ison(*params)   # args: list of nicks
        elif cmd == "join":
            self.NewChannelWindow(*params)
            self.connection.join(*params)   # args: channel; optional key
        elif cmd == "kick":
            self.connection.kick(*params)   # args: channel, nick; optional comment
        elif cmd == "links":
            self.connection.links(*params)
        elif cmd == "list":
            self.connection.list(*params)   # optional args: channel, server
        elif cmd == "lusers":
            self.connection.lusers(*params) # optional arg: server
        elif cmd == "mode":
            self.connection.mode(target=params[0], command=params[1])
        elif cmd == "motd":
            self.connection.motd(*params)   # optional arg: server
        elif cmd == "names":
            self.connection.names(*params)  # optional arg: channels
        elif cmd == "nick":
            self.connection.nick(newnick=params[0])
        elif cmd == "notice":
            self.connection.notice(target=params[0], text=params[1])
        elif cmd == "oper":
            self.connection.oper(oper=params[0], password=params[1])
        elif cmd == "part":
            self.connection.part(params)   # optional arg: (list of) channels
        elif cmd == "pass":
            self.connection.pass_(password=params[0])
        elif cmd == "ping":
            self.connection.ping(params)
        elif cmd == "pong":
            self.connection.pong(params)

        elif cmd in ("msg","privmsg"):
            if len(params) == 0:
                raise "MSGError", "You must supply the target and the message"
            target = params[0]
            if len(params) == 2:
                text = params[1]
            else:
                text = " " .join(params[1:])
            print target, text
            self.connection.privmsg(target=target, text=text)
            # Displays out message in the window_channel
            if hasattr(window, "getChannelname"):
                window.addMessage(text, self.connection.get_nickname(),target)
            else:   # window status
                window.ServerEvent("[%s(%s)] %s" % ("msg", target, text))

        elif cmd == "privmsg_many":
            self.connection.privmsg_many(*params)   # args: targets, text

        elif cmd == "quit":
            self.connection.quit(*params)       # optional message
            # Stop checking for events
            self.statuswindow.disableChecking()
            
        elif cmd == "sconnect":
            self.connection.sconnect(*params)   # args: target; optional: port, server
        elif cmd == "squit":
            self.connection.squit(*params)      # args: server; optional: comment
        elif cmd == "stats":
            self.connection.stats(*params)      # args: statstype; optional: server
        elif cmd == "time":
            self.connection.time(*params)       # optional: server
        elif cmd == "topic":
            self.connection.topice(*params)     # args: channel and optional: new_topic
        elif cmd == "trace":
            self.connection.trace(*params)      # optional: target
        elif cmd == "user":
            self.connection.user(username=params[0], realname=params[1])
        elif cmd == "userhost":
            self.connection.userhost(*params)   # arg: nicks
        elif cmd == "users":
            self.connection.users()
        elif cmd == "version":
            self.connection.version(*params)    # optional: server
        elif cmd == "wallops":
            self.connection.wallops(text=params[0])
        elif cmd == "who":
            self.connection.who(*params)        # optional: target, op
        elif cmd == "whois":
            self.connection.whois(targets=params[0])
        elif cmd == "whowas":
            self.connection.whowas(*params)     # args: nick; optional: max, server

        # commands used only for development purposes
        elif cmd == "debug":
            self.setDebug(True)
        elif cmd == "nodebug":
            self.setDebug(False)

        elif cmd == "joindebug":
            window = self.NewChannelWindow("Debug window")
#            window.setUsers(["test", "toto"])
        elif cmd == "check":
            self.checkEvents()

    def checkEvents(self):
        """Redirects all received events to the correct windows."""
        # Print events and display them in the rigth windows.
        for e in self.getEvents():

            etype = e.eventtype()

            # Skip raw messages.
            if etype == "all_raw_messages": 
                continue
            # Print event.
            text="\nEvent: %s\nSource: %s\nTarget: %s\nArguments: %s" % (
                    etype,
                    e.source(),
                    e.target(),
                    e.arguments()
                    )
            print text

            # Events to display in the status window.
            if etype == "welcome":
                self.host = e.source()
                self.statuswindow.SetCaption(self.host)
                for arg in e.arguments():
                    self.statuswindow.ServerEvent(arg)

            elif etype == "privnotice":
                text = ""
                if e.source() and e.source().startswith("NickServ"):
                    text = "NickServ: " + e.arguments()[0]
                    self.statuswindow.ServerEvent(text)
                elif e.source() and e.source().startswith("MemoServ"):
                    text = "MemoServ: " + e.arguments()[0]
                    self.statuswindow.ServerEvent(text)
                else:   # is it possible?
                    self.statuswindow.ServerEvent(e.arguments()[0])
                    
            elif etype == "umode":
                self.statuswindow.ServerEvent("umode: "+e.arguments()[0])
                
            elif etype in ("motd", "motdstart", "endofmotd"):
                self.statuswindow.ServerEvent(e.arguments()[0])

            # Events to display in the channel windows.
            elif etype in ("topic", "topicinfo", "nochanmodes"):
                args = e.arguments()
                chan = args.pop(0)  # Channel name where the message come
                                    # from.
                # find out the corresponding window
                window = self.getWindowChannelRef(chan)
                if window:
#                    if len(args) > 1:
#                        args = " ".join(args)
#                    else:
#                        args = args[0]
                    args = " ".join(args)
                    text = "[%s] %s" % (etype, args)
                    window.addRawText(text)

            elif etype == "namereply":
                chan = e.arguments()[1]
                window = self.getWindowChannelRef(chan)
                if window:
                    users = e.arguments()[2].split()
                    # TODO add users to user list (see window_channel.py)
                    window.setUsers(users)
                    
            elif etype == "pubmsg":
                chan = e.target()
                window = self.getWindowChannelRef(chan)
                if window:
                    window.addMessage(e.arguments()[0], e.source())
                    
            elif etype == "join":
                chan = e.target()
                window = self.getWindowChannelRef(chan)
                if window:
                    text = "%s has joined %s" % (e.source(), chan)
                    window.addRawText(text)
                    # TODO update users' list

            elif etype == "part":
                window = self.getWindowChannelRef(e.target())
                if window:
                    text = "%s has leaved %s" % (e.source(), e.target())
                    window.addRawText(text)
                    # TODO update users' list when it'll work
