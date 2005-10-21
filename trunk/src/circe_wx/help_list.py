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

# STANDARD HELP FORMAT: <command which searched for>,[-|<text here>|-]
# Example: server,[-|\n/server server [port] [nickname] [channels]|-]

def parse_document(doc="doc/help_list"):
    global help_list
    help_list = {}
    a = open(doc, "r")
    for line in a.readlines():
        command = line.split(",")[0] # gets the command
        text = " ".join(line.split(",")[1:])[" ".join(line.split(",")[1:]).find("(|")+2:" ".join(line.split(",")[1:]).find("|)")]
        help_list[command] = text
    a.close()

def grab_value(value):
    if value.strip() != "":
        try:
            return help_list[value].replace("\\n", "\n").replace("\\t", "\t")
        except KeyError:
            return "Error: Unknown Command \"%s\"" % (value)
    else:
        a = grab_all_keys()
        tmpb = ""
        for obj in a:
            tmpb += obj+"\n"
        return tmpb
def grab_all_keys():
    lst = []
    for obj in help_list:
        lst.append(obj)
    return lst
