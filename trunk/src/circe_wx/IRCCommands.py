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

