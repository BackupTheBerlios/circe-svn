import os
import commands

class Parser(commands.Command):
    
    def execute(self, event, window, cmd, *args):
        if not cmd:
            return
        
        if not cmd.startswith('/'):
            return False # propagate
    
        for command in commands.COMMAND:
            if command != self and command.name == cmd:
                return command.execute(event, window, cmd, *args)
        	
