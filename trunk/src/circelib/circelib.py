import socket, circe_globals
class Server:
    def __init__(self, host, port=6667):
        global IC
        IC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(host, port)
        IC.connect(host,int(port))
    def nick(self, nick, user, host):
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
    def closeConnection(self):
        quitmsg = circe_globals.QUITMSG
        IC.send("QUIT %s\r\n" % (str(quitmsg)))
        IC.close()
    def sendAction(self, channel, action):
        IC.send("PRIVMSG %s :\001ACTION %s\001" % (channel, action))
    def sendMode(self, channel, mode, args):
        IC.send("MODE %s %s %s" % (channel, mode, args))
    def sendKick(self, channel, person, reason):
        IC.send("KICK %s %s %s" % (channel, person, reason))
    def chanTopic(self, channel, nt):
        IC.send("TOPIC %s %s" % (channel, nt))
