from calculator import Command

class ModulusCommand(Command):
    def execute(self, *args):
        return float(args[0]) % float(args[1])

COMMANDS = {
    "modulus": ModulusCommand()
}

