import socket
class server:
    def __init__(self, server, port=6667):
        global IC, server
        IC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IC.connect(server,int(port))
    def nick(self, nick, user):
        IC.send("USER %s %s %s %s\r\n" % (nick, user,server,user))
        IC.send("NICK %s %s\r\n" % (nick, user))
    def send(self, ts):
        IC.send("%s\r\n" % (ts))
    def nickChange(self, newnick):
