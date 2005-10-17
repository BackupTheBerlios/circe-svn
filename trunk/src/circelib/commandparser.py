# INSERT GPL HEADER HERE

# Circe	Command class

class Error(Exception): pass

class Command(object):
    def __init__(self, server):
        self.server = server
