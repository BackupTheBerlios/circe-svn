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

# Core IRC Commands Library
import string, help_list, config_engine
import circelib.dialogs as dialogs

class IRCCommands:
    def __init__(self):
        self.config = config_engine.Config()
        help_list.parse_document()
    def cmd_server(self,window,server,params):
        if len(params) <= 0:
            window.server_event(help_list.grab_value("server"))
            return

        d = {}; d["server"] = params[0]
        try:
            port = d['port'] = int(params[1])
        except (IndexError, ValueError):
            port = d['port'] = 6667
        try:
            nickname = d['nickname'] = params[2]
        except IndexError:
            try: nickname = d['nickname'] = self.config["nickname"]
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
            if not channels: return
            server.connection.join(*channels)
            return

        server.connect("server", window, **d)
        self.host = server
        # Ensures checking for new events is enabled.
        server.statuswindow.enable_checking()
        channels = params[3:]
        if not channels: return
        server.connection.join(*channels)

    def cmd_clear(self,window,server,params):
        window.txt_buffer_clr()
     
    def cmd_echo(self,window,server,params):
        window.server_event(" " .join(params))

    def cmd_join(self,window,server,params):
         server.connection.join(*params)
         window.server_event("%s has joined %s." % (server.connection.get_nickname(), params[0]))

    def cmd_action(self,window,server,params):
         if len(params) >= 1:
             server.connection.action(target=window.get_channelname(), action=' '.join(params[0:]))
             window.server_event('* %s %s' % (server.connection.get_nickname(), ' '.join(params[0:])))

    def cmd_topic(self,window,server,params):
         if len(params) <= 0:
             server.connection.topic(channel=window.get_channelname())
         else:
             if params[0][0] == "#" and params[0] in server.get_channels(): # got a channel
                 if len(params) >= 2: # got a topic too!
                     server.connection.topic(channel=params[0], new_topic=" ".join(params[1:]))
                 else: # just got a channel
                     server.connection.topic(channel=params[0])
             else:
                  server.connection.topic(channel=window.get_channelname(), new_topic=" ".join(params[0:]))

    def cmd_globops(self,window,server,params):
         server.connection.globops(params[0])

    def cmd_help(self,window,server,params):
         if len(params) > 0:
             help_list.grab_value(window, params[0])
         else:
             help_list.grab_value(window, "")

    def cmd_invite(self,window,server,params):
         if len(params) <= 0:
             help_list.grab_value(window, "invite")
         elif len(params) == 1 and params[0] not in server.get_channels():
             server.connection.invite(nick=params[0], channel=window.get_channelname())
         elif len(params) == 1 and params[0] in server.get_channels():
             help_list.grab_value(window, "invite")
         elif len(params) == 2 and params[0] in server.get_channels() and params[1] not in server.get_channels():
             server.connection.invite(nick=params[0], channel=params[1])

    def cmd_info(self,window,server,params):
        if len(params) <= 0 :
            server.connection.info("")
        else:
            server.connection.info(params[0])

    def cmd_ison(self,window,server,params):
        if len(params) <= 0:
            help_list.grab_value(window, 'ison')
            return
        if ',' in params[0]:
            server.connection.ison(params[0].split(','))
        else:
            server.connection.ison(params)

    def cmd_kick(self,window,server,params):
        if len(params) <= 0:
            help_list.grab_value(window, "kick")

        elif len(params) == 1: 
            if params[0] in server.get_channels():
                help_list.grab_value(window, "kick")
            elif params[0] not in server.get_channels():
                server.connection.kick(window.get_channelname(), params[0], server.connection.get_nickname())

        elif len(params) == 2:
            if params[0] in server.get_channels():
                help_list.grab_value(window, "kick")
            elif params[0] not in server.get_channels() and params[1] in server.get_channels():
                server.connection.kick(params[1], params[0], server.connection.get_nickname())
            elif params[0] not in server.get_channels() and params[1] not in server.get_channels():
                server.connection.kick(window.get_channelname(), params[0], " ".join(params[1:]))

        elif len(params) >= 3:
            if params[0] in server.get_channels():
                help_list.grab_value(window, "kick")
            elif params[0] not in server.get_channels and params[1] in server.get_channels():
                server.connection.kick(params[1], params[0], " ".join(params[2:]))
            elif params[0] not in server.get_channels() and params[1] not in server.get_channels():
                server.connection.kick(window.get_channelname(), params[0], " ".join(params[1:]))

    
    def cmd_links(self,window,server,params):
        if len(params) <= 0:
            server.connection.links("", "")
        elif len(params) == 1:
            server.connection.links(params[0], "")
        elif len(params) == 2:
            server.connection.links(params[0], params[1])
 
