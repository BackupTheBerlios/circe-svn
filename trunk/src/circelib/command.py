# INSERT GPL HEADER HERE

# Circe	Command class
import utils
import getopt

class Error(Exception): pass
methods = {}
class Command(object):
    def __init__(self, server, **kwargs):
        self.server = server
        
        klass = type(self) # NOT self.__class__ as it is "<type 'type'>"
        try:
            respond_to = klass.respond_to
        except AttributeError:
            raise Error, "%s doesn't have a respond_to attribute." % klass.__name__

        self.methods = methods
        
        if len(respond_to) == 1:
            method = respond_to[0]
            # this class only responds to one command, give this one execute instead
            if not getattr(self, 'execute', None):
                raise Error, "%s has no method %s" % (klass.__name__, 'execute')
            self.methods[m] = (self, self.execute)
            return
        
        for cmd in respond_to:
            method = getattr(self, 'do_%s' % cmd, None)
            if not method:
                raise Error, "%s responds to the command %s, but no method %s exists in %s" % (klass.__name__, cmd, 'do_%s' % cmd, klass.__name__)
            self.methods[cmd] = (self, method)
        else:
            if len(respond_to) > 0:
                return
            raise Error, "%s doesn't respond to anything." % klass.__name__
            
    def parse(self, cmdstring, window, server):
         if cmdstring[0] == "/":
             cmdstring = cmdstring[1:]
         else:
             if hasattr(window, "get_channelname"):
                 target = window.get_channelname()
                 server.connection.privmsg(target, cmdstring)
                 mynick = server.connection.get_nickname()
                 window.add_message(cmdstring, mynick)
             return
         
         params = cmdstring.split(' ')
         command = params.pop(0)
         params = self.parse_options(params)
         try:
             method = self.methods[command]
         except KeyError:
             window.server_event('Unknown command /%s' % cmd)
             return
         return method(command, window, server)
    def do_(self, *args): pass

def find_command(cmd_string):
    for cmd in methods.iterkeys():
        command_tuple = methods[cmd]
        command_instance = command_tuple[0]
        if cmd_string in cmd:
            return command_instance
    return None
