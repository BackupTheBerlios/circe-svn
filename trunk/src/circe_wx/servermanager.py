from circelib.circelib import Server

servers = []
        
def AddServer(*options):
    s = Server(*options)
    servers.append(s)
    return s

def RemoveServer(s):
    if s in servers:
        del servers[s]

def TextCommand(s,cmdstring):
    if(cmdstring == None or len(cmdstring) == 0):
        raise "Empty command"
    # Strip /
    if cmdstring[0] == "/":
        cmdstring = cmdstring[1:]
    # Create a list
    cmdlist = cmdstring.split()
    cmd = cmdlist[0]
    params = cmdlist[1:]
    if(cmd == "server"):
        s.connect(*params)
    elif(cmd == "join"):
        s.joinChannel(*params)
    elif(cmd == "nick"):
        s.nick(*params)
