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
from circelib.errors import *
import circelib.dialogs as dialogs
import config_engine
import help_list

class WXServer(Server):
    def __init__(self,windowarea):
        Server.__init__(self)
        c = self.connection
        self.host = c.connected and c.get_server_name() or None
        self.statuswindow = WindowStatus(windowarea,self)
        self.windowarea = windowarea
        self.channels = []
        self.config = config_engine.Config()
        help_list.parse_document()
        self.commands = IRCCommands()
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
        """Return the WindowChannel object bound to channelname or False if
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

    def get_help(self, window, command):
        window.server_event(help_list.grab_value(command))

    def text_command(self,cmdstring,window):
        if not cmdstring:
            return
    
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
                for line in cmdstring.split("\n"):
                    if line.strip().strip("\n"):
                        self.connection.privmsg(target, line.encode('utf-8'))
                        mynick = self.connection.get_nickname()
                        window.add_message(line, mynick)
            return

        # Create a list
        params = cmdstring.split()
        cmd = params.pop(0)
        if self.debug:
            print params
        cmd = cmd.lower()
        # Find out what command is being executed
        if cmd == "server":
            self.commands.cmd_server(window,self,params)

        elif cmd == "newserver":
            d = {}
            server = d['server'] = params[0]
            try:
                port = d['port'] = int(params[1])
            except (IndexError, ValueError):
                port = d['port'] = 6667
            try:
                nickname = d['nickname'] = params[2]
            except IndexError:
                try:
                    nickname = d['nickname'] = self.config["nickname"]
                except KeyError:
                    result = dialogs.ask_nickname()
                    if not result:
                        window.server_event("Nickname defaulting to 'irc'.")
                        nickname = d['nickname'] = 'irc'
                    else:
                        nickname = d['nickname'] = result

            s = self.new_status_window()
            s.connect(cmd, window, **d)
            self.host = server
            s.statuswindow.enable_checking()
            channels = params[3:]
            if not channels:
                return
            self.connection.join(*channels)
            return

        
        elif cmd == "echo":
            window.server_event(" " .join(params))

        elif cmd == "action" or cmd == "me":
            try:
                params[0]
                if params[0][0] != '#':
                    raise IndexError
            except IndexError:
                params.insert(0, window.get_channelname())
            self.connection.action(target=params[0], action=' '.join(params[1:]))
            window.server_event('* %s %s' % (self.connection.get_nickname(), ' '.join(params[1:])))
        elif cmd == "connect":
            if not self.connection.is_connected():
                window.server_event("You are not connected to a server. Please use /server instead.")
                return
            server = params[0]
            try:
                port = int(params[1])
            except (IndexError,ValueError):
                port = 6667

            self.connect(server, port, self.connection.get_nickname())
        elif cmd == "globops":
            self.connection.globops(params[0])
        elif cmd == "help":
            if len(params) >= 1:
                self.get_help(window, params[0])
            else:
                self.get_help(window, "")
        elif cmd == "info":
            self.connection.info(params and params[0] or "")
        elif cmd == "invite":
            try:
                params[0], params[1]
            except IndexError:
                window.server_event('/invite syntax: /invite nick channel')
                return
            self.connection.invite(nick=params[0], channel=params[1])

        elif cmd == "ison":
            if not params:
                window.server_event('/ison syntax: /ison nick [...]')
                return
            # The user separated the parameters by a comma
            if ',' in params[0]:
                nicks = params[0].split(',')
            # The parameters have been split in a list
            else:
                nicks = params
            self.connection.ison(nicks)

        elif cmd == "join" or cmd == "j":
            self.connection.join(*params)
            window.server_event("%s has joined %s." % (self.connection.get_nickname(), params[0]))
        elif cmd == "kick" or cmd == "k":
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
            target = params[0]
            command = " ".join(params[1:])
            if not target or not command:
                window.server_event('/mode target command(s)')
                return
            self.connection.mode(target=target, command=command)

        elif cmd == "motd":
            self.connection.motd(params and params[0] or "")

        elif cmd == "names":
            if params[0]:
                if "," in params[0]:
                    # Assumes channels are in comma separated list.
                    channels = params[0].split(",")
                elif ' ' in params[0]:
                    # Channels given as multiple args "#chan1 #chan2 #chan3"
                    channels = params[0].split()

                self.connection.names(channels)

        elif cmd == "nick":
            oldnick=self.connection.get_nickname()
            try:
                nick = params
            except IndexError:
                window.server_event("/nick syntax: /nick newnick")
                return
            self.connection.nick(newnick=params[0])
            window.server_event("%s is now known as %s" % (oldnick, params[0]))
        elif cmd == "notice":
            try:
                target, text = params
            except ValueError:
                window.server_event("/notice syntax: /notice target message")
                return
            self.connection.notice(target=params[0], text=params[1])
        elif cmd == "oper":
            try:
                oper, password = params
            except IndexError:
                window.server_event("/oper syntax: /oper oper pass")
                return
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
            try:
                params[0]
            except IndexError:
                window.server_event("/pass syntax: /pass password")
                return
            self.connection.pass_(password=params[0])

        elif cmd == "ping":
            try:
                target1 = params[0]
            except IndexError:
                window.server_event("/ping syntax: from [to]")
                return
            target2 = ""
            if len(params) > 1:
                target2 = params[1]
            self.connection.ping(target1, target2)

        elif cmd == "pong":
            try:
                target1 = params[0]
            except IndexError:
                window.server_event("/pong syntax: from [to]")
                return
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
            if not params:
                try: quitmsg = self.config["quitmsg"]
                except: quitmsg = circe_globals.QUITMSG
                self.connection.quit(quitmsg)
                return
            else:
                self.connection.quit(" ".join(params))

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
            try:
                params[0]
                if params[0] != "#":
                    raise IndexError
                if params[0] not in self.channels:
                    del params[0]
                    raise IndexError
            except IndexError:
                params.insert(0, window.get_channelname())
            result = params[1:]
            if result:
                self.connection.topic(channel=params[0], new_topic=result)
            else:
                self.connection.topic(channel=params[0])

            if new_topic:
                if params[0] in self.channels or params[0].startswith("#"):
                    new_topic = " ".join(params[1:])
                    if new_topic:
                        self.connection.topic(channel=param[0], new_topic=" ".join(param[1:]))
                    else:
                        if params[0].strip() != "":
                              self.connection.topic(channel=params[0])
                        else: 
                              self.connection.topic(channel=window.get_channelname())
                else: 
                    self.connection.topic(channel=window.get_channelname(), new_topic=new_topic)
            else:
                self.connection.topic(channel=window.get_channelname())
        elif cmd == "trace":
            self.connection.trace(params and params[0] or "")
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
            self.setdebug(True)

        elif cmd == "nodebug":
            self.setdebug(False)

        elif cmd == "check":
            self.check_events()
	elif cmd == "clear":
            window.txt_buffer_clr()
	else:
            window.server_event("%s: Invalid Command" % (cmd))
    def check_events(self):
        """Redirects all received events to the correct windows."""
        # Print events and display them in the rigth windows.
        for e in self.get_events():

            etype = e.eventtype()
            # Skip raw messages.
            if etype == "all_raw_messages": 
                continue

            elif etype == "action":
                target = e.target()
                source = irclib.nm_to_n(e.source())
                action = e.arguments()
                if len(action) > 1:
                    action = action[1:]
                action = ' '.join(action)
                window = self.get_channel_window(target)
                if not window: continue
                to_server  = '* %s %s' % (source, action)
                window.server_event(to_server)

            # Events to display in the status window.
            elif etype == "welcome":
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
                if len(args) > 1:
                    chan = args.pop(0)  # Channel name where the message comes
                                        # from.
                    topic = [] # store topic in here
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
                    else:
                        window = self.get_channel_window("CURRENT")
                        args = " ".join(args)
                        if etype == "topic":
                            text = "Topic for %s is: %s" % (chan, args)
                        window.server_event(text)
                else:
                    window = self.get_channel_window(e.target())
                    if window:
                        window.server_event("%s has changed the topic of %s to: %s" % (e.source().split("!")[0], e.target(), args[0]))

            elif etype == "topicinfo":
                sender = e.arguments()[1]
                timeago = int(e.arguments()[2])
                date = time.asctime(time.gmtime(timeago))

                window = self.get_channel_window(e.arguments()[0])
                if window:
                    text = "Topic for %s set by %s on %s" % (e.arguments()[0], sender, date)
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
                if irclib.is_channel(target):
                    win = self.get_channel_window(target)
                    if win:
                        win.add_message(text, source, target)
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
                    source = irclib.nm_to_n(src)
                    text = "%s has joined %s" % (source, chan)
                    window.server_event(text)
                    window.users([source])

            elif etype == "part":
                chan = e.target()
                src = e.source()
                arguments = e.arguments()
                nickname = irclib.nm_to_n(src)
                window = self.get_channel_window(chan)

                if nickname == self.connection.get_nickname():
                    if window:
                        self.remove_channel_window(chan)
                        return
                if window:
                    args = ' '.join(arguments)
                    if not args:
                        text = "%s (%s) has left %s" % (nickname, src, chan)
                    else:
                        text = "%s (%s) has left %s: %s" % (nickname, src, chan, args)
                    window.server_event(text)
                    window.del_user([nickname])

            elif etype == "quit":
                # Informs each channel that the user has quit.
                for chan in self.channels:
                    chan.user_quit(e)

            elif etype == "nicknameinuse":
                nickname = e.arguments()[0]
                try:
                    self.connection.nick(self.config["secondary_nickname"])
                except KeyError:
                    result = dialogs.ask_nickname(nickname)
                    if result:
                        self.connection.nick(result)
                    else:
                        self.connection.nick(nickname+"_")
                text = "%s: %s" % (nickname, e.arguments()[1])
                self.statuswindow.server_event(text)

            elif etype == "nick":
                for chan in self.channels:
                    chan.nick_changed(e)

            elif etype == "error":
                pass

            elif etype == "disconnect":
                text = "%s (%s)" % (e.arguments()[0], e.source())
                self.statuswindow.server_event(text)
                self.statuswindow.evt_disconnect()

class IRCCommands:
    def __init__(self):
        self.config = config_engine.Config()
        help_list.parse_document()
    def cmd_server(self,window,server,params):
        if len(params) <= 0: 
            window.server_event(help_list.grab_value("server"))
            return

        d = {}
        d["server"] = params[0]

        try:
            port = d['port'] = int(params[1])
        except (IndexError, ValueError):
            port = d['port'] = 6667

        try:
            nickname = d['nickname'] = params[2]
        except IndexError:

            try:
                nickname = d['nickname'] = self.config["nickname"]

            except KeyError:
                result = dialogs.ask_nickname()
                if not result:
                    window.server_event("Nickname defaulting to 'irc'.")
                    nickname = d['nickname'] = 'irc'
                else:
                    nickname = d['nickname'] = result

        # If we're already connected to a server, opens a new connection in
        # another status window.
        if server.is_connected():
            s = server.new_status_window()
            s.connect(cmd, window, **d)
            self.host = server
            s.statuswindow.enable_checking()
            channels = params[3:]
            if not channels:
                return
            server.connection.join(*channels)
            return
 
        server.connect("server", window, **d)
        self.host = server
        # Ensures checking for new events is enabled.
        server.statuswindow.enable_checking()
        channels = params[3:]
        if not channels:
            return
        server.connection.join(*channels)

