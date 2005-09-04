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

import time

import irclib

from window_status import WindowStatus
from window_channel import WindowChannel
from circelib.server import Server

class WXServer(Server):
    def __init__(self,windowarea):
        Server.__init__(self)
        c = self.connection
        self.host = c.connected and c.get_server_name() or None
        self.statuswindow = WindowStatus(windowarea,self)
        self.windowarea = windowarea
        self.channels = []

    def get_hostname(self):
        """Return the host we are connected to."""
        return self.host

    def is_connected(self):
        return self.connection.is_connected()

    def new_channel_window(self,channelname):
        """Open a new channel window, sets the caption and stores it."""

        # Avoid to create the same window multiple times.
        if channelname in [w.get_channelname() for w in self.channels]:
            raise "WindowChannel %s already exists" % channelname

        new = WindowChannel(self.windowarea,self,channelname)
#        new.set_caption(caption)
        self.channels.append(new)
        self.windowarea.show_window(self, new)
        return new

    def remove_channel_window(self, channelname):
        """Remove the channel window if it exists."""
        win = self.get_channel_window(channelname)
        if not win:
            return
        win.close()

    def channel_closed(self, channel):
        if channel in self.channels:
            del self.channels[self.channels.index(channel)]
        else:
            return
    def get_channel_window(self, channelname):
        """Return the WindowChannel object binded to channelname or False if
        it does not match.
        """
        for window in self.channels:
            if window.get_channelname() == channelname:
                return window
        return False

    def new_status_window(self):
        """Open a new status window."""
        s = self.windowarea.add_server()
        self.windowarea.show_window(s.statuswindow.section_id, s.statuswindow)
        return s

    def text_command(self,cmdstring,window):
        if not cmdstring:
            return # is raising a exception necessary?
	
        # in a debug window, do nothing
        if hasattr(window, "get_channelname") and \
            window.get_channelname() == "debug":
            return

        # Strip /
        if cmdstring[0] == "/":
            cmdstring = cmdstring[1:]
        else:
            # if it is not a command send the message to the channel
            if hasattr(window, "get_channelname"):
                target = window.get_channelname()
                self.connection.privmsg(target, cmdstring)
                mynick = self.connection.get_nickname()
                window.add_message(cmdstring, mynick)
            return

        # Create a list
        params = cmdstring.split()
        cmd = params.pop(0)
        if self.debug:
            print params

        # Find out what command is being executed
        if cmd == "server":
            # /server servername [nickname]
            if len(params) < 1:
                window.server_event("/server syntax: /server servername [nick]")
                return
            server = params[0]
            try:
                nick = params[1]
            except IndexError:
                nick = "circe"
            try:
                port = int(params[3])
            except (IndexError,ValueError):
                port = 6667

            # If we're already connected to a server, opens a new connection in
            # another status window.
            if self.is_connected():
                s = self.new_status_window()
                s.connect(server, port, nick)
                self.host = server
                s.statuswindow.enable_checking()
                return

            self.connect(server=server, port=port, nickname=nick)
            self.host = server
            # Ensures checking for new events is enabled.
            self.statuswindow.enable_checking()

        elif cmd == "action" or cmd == "me":
            self.connection.action(target=params[0], action=params[1])
        elif cmd == "connect":
            if not self.connection.is_connected():
                window.server_event("You are not connected to a server. Please use /server instead.")
                return
            server = params[0]
            try:
                port = int(params[1])
            except (IndexError,ValueError):
                port = 6667
            #try:
            #   remote_server = params[2]
            #except IndexError:
            #   pass

            self.connect(server, port, self.connection.get_nickname())
        elif cmd == "globops":
            self.connection.globops(params[0])
        elif cmd == "info":
            self.connection.info(params and params[0] or "")
        elif cmd == "invite":
            self.connection.invite(nick=params[0], channel=params[1])

        elif cmd == "ison":
            if ',' in params[0]:
                nicks = params[0].split(',')
            elif ' ' in params[0]:
                nicks = params[0].split(' ')
            else: nicks = params[0]
            self.connection.ison(nicks)

        elif cmd == "join":
            self.connection.join(*params)

        elif cmd == "kick":
            try:
                channel = params[0]
            except IndexError:
                channel = window.get_channelname()
            try:
                nick = params[1]
            except IndexError:
                window.server_event("/kick syntax: /kick [channel] nickname [comment]")
                return
            try:
                comment = params[2]
            except IndexError:
                comment = ""
            self.connection.kick(channel, nick, comment)

        elif cmd == "links":
            remote_server = ""
            server_mask = ""
            if len(params) > 0:
                remote_server = params[0]
                if len(params) > 1:
                    server_mask = params[1]

            self.connection.links(remote_server, server_mask)

        elif cmd == "list":
            channels = None
            server = ""
            if len(params) > 0:
                channels = params[0]
                if len(params) > 1:
                    server = params[1]
            self.connection.list(channels, server)

        elif cmd == "lusers":
            self.connection.lusers(params and params[0] or "")

        elif cmd == "mode":
            command = " ".join(params[1:])
            self.connection.mode(target=params[0], command=command)

        elif cmd == "motd":
            self.connection.motd(params and params[0] or "")

        elif cmd == "names":
            if params[0]:
                if "," in params[0]:
                    # Assumes channels are in comma separated list.
                    channels = params[0].split(",")
                elif ' ' in params[0]:
                    # Channels given as multiple args "#chan1 #chan2 #chan3"
                    channels = params[0]

                self.connection.names(channels)

        elif cmd == "nick":
            try:
                params[0]
            except IndexError:
                window.server_event("/nick syntax: /nick newnick")
                return
            self.connection.nick(newnick=params[0])

        elif cmd == "notice":
            try:
                params[0], params[1]
            except IndexError:
                window.server_event("/notice syntax: /notice target message")
                return
            self.connection.notice(target=params[0], text=params[1])
        elif cmd == "oper":
            self.connection.oper(oper=params[0], password=params[1])

        elif cmd == "part":
            try:
                params[0]
            except IndexError:
                chans = ['%s' % window.get_channelname()]
                self.connection.part(chans)
                return
            if ',' in params[0]:
                chans = params[0].split(",")
            elif ' ' in params[0]:
                chans = params[0].split(' ')
            else:
                chans = [params[0]]
            self.connection.part(chans)

        elif cmd == "pass":
            self.connection.pass_(password=params[0])

        elif cmd == "ping":
            target1 = params[0]
            target2 = ""
            if len(params) > 1:
                target2 = params[1]
            self.connection.ping(target1, target2)

        elif cmd == "pong":
            target1 = params[0]
            target2 = ""
            if len(params) > 1:
                target2 = params[1]
            self.connection.pong(target1, target2)

        elif cmd in ("msg","privmsg"):
            if not params:
                window.server_event("/msg syntax: /msg target text")
                return
            target = params[0]
            text = " " .join(params[1:])
            self.connection.privmsg(target, text)
            # Displays out message in the WindowChannel
            if hasattr(window, "get_channelname"):
                window.add_message(text, self.connection.get_nickname(),target)
            else:   # window status
                window.server_event("[%s(%s)] %s" % ("msg", target, text))

        elif cmd == "privmsg_many":
            targets = params[0]
            text = " ".join(params[1:])
            self.connection.privmsg_many(targets, text)

        elif cmd == "quit":
            self.connection.quit(" ".join(params) or "")

        elif cmd == "sconnect":
            self.connection.sconnect(params[0],
                                    len(params) > 1 and params[1] or "",
                                    len(params) > 2 and params[2] or ""
                                    )
        elif cmd == "squit":
            self.connection.squit(params[0],
                                    len(params) > 1 and params[1] or ""
                                    )
        elif cmd == "stats":
            query = params[0]   # either l, m, o or u as defined in the rfc
            if len(params) > 1:
                server = params[1]
            else:
                server = ""
            self.connection.stats(query, server)

        elif cmd == "time":
            server = params[0]
            self.connection.time(server)
            
        elif cmd == "topic":
            new_topic = " ".join(params[1:])
            self.connection.topic(channel=params[0], new_topic=new_topic)

        elif cmd == "trace":
            self.connection.trace(params and params[0] or "")
        elif cmd == "user":
            try:
                username, realname = params[0], params[1]
            except (ValueError,IndexError):
                window.server_event("/user syntax: /user username realname")
                return
            self.connection.user(username=params[0], realname=params[1])

        elif cmd == "userhost":
            if params:
                if ',' in params[0]:
                    nicks = params[0].split(",")
                elif ' ' in params[0]:
                    nicks = params[0].split(" ")
            self.connection.userhost(nicks)

        elif cmd == "users":
            self.connection.users(params and params[0] or "")

        elif cmd == "version":
            self.connection.version(params and params[0] or "")

        elif cmd == "wallops":
            self.connection.wallops(text=params[0])

        elif cmd == "who":
            self.connection.who(params and params[0] or "",
                                len(params) > 1 and params[1] or ""
                                )
        elif cmd == "whois":
            self.connection.whois(targets=params[:1])
        elif cmd == "whowas":
            self.connection.whowas(params[0],
                                    len(params) > 1 and params[1] or "",
                                    len(params) > 2 and params[2] or ""
                                    )
        elif cmd == "close":
            window.close()

        # commands used only for development purposes
        elif cmd == "debug":
            self.setdebug()

        elif cmd == "nodebug":
            self.nodebug()

        elif cmd == "check":
            self.check_events()

    def check_events(self):
        """Redirects all received events to the correct windows."""
        # Print events and display them in the rigth windows.
        for e in self.get_events():

            etype = e.eventtype()

            # Skip raw messages.
            if etype == "all_raw_messages": 
                continue

            # Events to display in the status window.
            if etype == "welcome":
                self.host = e.source()
                self.statuswindow.set_caption(self.host)
                for arg in e.arguments():
                    self.statuswindow.server_event(arg)

            elif etype == "privnotice":
                text = ""
                source = e.source()
                prefixes = ["Nick", "Memo", "Chan"]
                for prefix in prefixes:
                    if source and source.startswith("%sServ" % prefix):
                        text = "%sServ: %s" % (prefix, e.arguments()[0])
                        self.statuswindow.server_event(text)
                else:
                    self.statuswindow.server_event(e.arguments()[0])

            elif etype == "umode":
                self.statuswindow.server_event("umode: "+e.arguments()[0])

            elif etype in ("motd", "motdstart", "endofmotd"):
                self.statuswindow.server_event(e.arguments()[0])

            elif etype in ("info", "endofinfo"):
                self.statuswindow.server_event(e.arguments()[0])

            # Events to display in the channel windows.
            elif etype in ("topic", "nochanmodes"):
                args = e.arguments()
                chan = args.pop(0)  # Channel name where the message comes
                                    # from.
                topic = [] 
                # find out the corresponding window
                window = self.get_channel_window(chan)
                if window:
                    args = " ".join(args)
                    if etype == "topic":
                        text = "Topic for %s is: %s" % (chan, args)
                    else:
                        text = "[%s] %s" % (etype, args)
                    if etype == "topic":
                        topic.append(text)
                    else:
                        window.server_event(text)

            elif etype == "topicinfo":
                sender = e.arguments()[1]
                timeago = int(e.arguments()[2])
                date = time.asctime(time.gmtime(timeago))

                window = self.get_channel_window(e.arguments()[0])
                if window:
                    text = "Topic for %s set by %s on %s" % (e.arguments()[0], sender, date)
                    topic.append(text)
                    window.server_event("\n".join(topic))
                topic = []

            elif etype == "namreply":
                chan = e.arguments()[1]
                window = self.get_channel_window(chan)
                if window:
                    users = e.arguments()[2].split()
                    window.users(users)

            elif etype == "pubmsg":
                chan = e.target()
                window = self.get_channel_window(chan)
                if window:
                    source = e.source().split("!")[0]
                    window.add_message(e.arguments()[0], source)

            elif etype == "privmsg":
                source = e.source().split("!")[0]
                target = e.target()
                text = "<%s> %s" % (source, " ".join(e.arguments()))
                if irclib.is_channel(target):
                    win = self.get_channel_window(target)
                    if win:
                        win.server_event(text)
                else:
                    self.statuswindow.server_event(text)

            elif etype == "join":
                chan = e.target()
                src = e.source()

                if irclib.nm_to_n(src) == self.connection.get_nickname():
                    self.new_channel_window(chan)
                    # Ensures we get the topic info, users list,...
                    self.connection.topic(chan)
                    self.connection.names([chan])
                    return

                window = self.get_channel_window(chan)
                if window:
                    source = e.source().split("!")[0]
                    text = "%s has joined %s" % (source, chan)
                    window.server_event(text)
                    window.users([source])

            elif etype == "part":
                chan = e.target()
                src = e.source()
                window = self.get_channel_window(chan)

                if irclib.nm_to_n(src) == self.connection.get_nickname():
                    if window:
                        self.remove_channel_window(chan)
                        return
                if window:
                    text = "%s has left %s" % (src, chan)
                    window.server_event(text)
                    window.del_user([src.split("!")[0]])

            elif etype == "quit":
                # Informs each channel that the user has quit.
                for chan in self.channels:
                    chan.user_quit(e)

            elif etype == "nicknameinuse":
                text = "%s: %s" % (e.arguments()[0], e.arguments()[1])
                self.statuswindow.server_event(text)

            elif etype == "error":
                pass

            elif etype == "disconnect":
                text = "%s (%s)" % (e.arguments()[0], e.source())
                self.statuswindow.server_event(text)
                self.statuswindow.evt_disconnect()
