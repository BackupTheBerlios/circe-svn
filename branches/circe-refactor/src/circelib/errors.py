class Help(Exception):
    def __init__(self, command, help_msg):
        self.command = command
        self.help_msg = help_msg
        Exception.__init__(self)
    def __str__(self):
        return "/%s help: %s" % (command, help_msg)
