COMMANDS = {} # TODO: remove this global

class Command(object):
    def __init__(self, name):
        self.name = name
        COMMANDS[name] = self.execute
    def execute(self, event, window, cmd, *args): pass # override
