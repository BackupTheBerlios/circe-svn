from circe_shell.server import Server

servers = []

def AddServer(*options):
    s = Server(*options)
    servers.append(s)
    return s

def RemoveServer(s):
    if s in servers:
        del servers[s]

def TextCommand(server,cmdstring):
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
        server.Connect(*params)
    elif(cmd == "join"):
        server.Join(*params)
