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
        IC.send("NICK %s\r\n" % (newnick))
    def joinChannel(self, channel, channelpass):
        IC.send("JOIN %s %s\r\n" % (channel, channelpass))
    def partChannel(self, channel, partmessage):
        IC.send("PART %s %s\r\n" % (channel, partmessage))
    def sendMessage(self, channel, message):
        IC.send("PRIVMSG %s :%s\r\n" % (str(channel), str(message)))
    def closeConnection(self, quitmsg):
        IC.send("QUIT %s\r\n" % (str(quitmsg)))
        IC.close()
        
