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

import circelib.circeirc as irclib

from window_status import WindowStatus
from window_channel import WindowChannel
from circelib.server import Server
from circelib.errors import *
import circelib.dialogs as dialogs
import config_engine
import help_list
from IRCCommands import *

class WXServer(Server):
    def __init__(self,windowarea):
        Server.__init__(self)
        c = self.connection
        self.host = c.connected and c.get_server_name() or None
        self.statuswindow = WindowStatus(windowarea,self)
        self.windowarea = windowarea
        self.channels = []
        self.channels_s = []
        self.config = config_engine.Config()
        help_list.parse_document()
        self.commands = IRCCommands()

    def get_channels(self):
        """Returns the list of channels connected to"""
        return self.channels_s
  
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
        self.channels_s.append(channelname)
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
            if cmdstring[1] == "/": # user escaping
                cmdstring = cmdstring[1:]
                if hasattr(window, "get_channelname"):
                    target = window.get_channelname()
                    for line in cmdstring.split("\n"):
                        if line.strip().strip("\n"):
                            self.connection.privmsg(target, line.encode('utf-8'))
                            mynick = self.connection.get_nickname()
                            window.add_message(line, mynick)
                return
            else:
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
            self.commands.cmd_server(window,self,params)
        
        elif cmd == "echo":
            self.commands.cmd_echo(window,self,params)

        elif cmd == "action" or cmd == "me":
            self.commands.cmd_action(window,self,params)

        elif cmd == "connect":
            self.commands.cmd_server(window,self,params)

        elif cmd == "globops":
            self.commands.cmd_globops(window,self,params)

        elif cmd == "help":
            self.commands.cmd_help(window,self,params)

        elif cmd == "info":
            self.commands.cmd_info(window,self,params)

        elif cmd == "invite":
            self.commands.cmd_invite(window,self,params)

        elif cmd == "ison":
            self.commands.cmd_ison(window,self,params)

        elif cmd == "join" or cmd == "j":
            self.commands.cmd_join(window,self,params)

        elif cmd == "kick" or cmd == "k":
            self.commands.cmd_kick(window,self,params)

        elif cmd == "links":
            self.commands.cmd_links(window,self,params)
 
        elif cmd == "list":
            self.commands.cmd_list(window,self,params)

        elif cmd == "lusers":
            self.commands.cmd_lusers(window,self,params)

        elif cmd == "mode":
            self.commands.cmd_mode(window,self,params)

        elif cmd == "motd":
            self.commands.cmd_motd(window,self,params)

        elif cmd == "names":
            self.commands.cmd_names(window,self,params)

        elif cmd == "nick":
            self.commands.cmd_nick(window,self,params)
 
        elif cmd == "notice":
            self.commands.cmd_notice(window,self,params)

        elif cmd == "oper":
            self.commands.cmd_oper(window,self,params)

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
            self.commands.cmd_topic(window,self,params)

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
            self.commands.cmd_clear(window,self,params)
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
                        else:
                            text = "[%s] %s" % (etype, args)
                        topic.append(text)
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

