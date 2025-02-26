import os
import importlib
import pkgutil
from abc import ABC, abstractmethod

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

# Concrete Command Classes
class AddCommand(Command):
    def execute(self, *args):
        return sum(map(float, args))

class SubtractCommand(Command):
    def execute(self, *args):
        return float(args[0]) - sum(map(float, args[1:]))

class MultiplyCommand(Command):
    def execute(self, *args):
        result = 1
        for num in args:
            result *= float(num)
        return result

class DivideCommand(Command):
    def execute(self, *args):
        try:
            result = float(args[0])
            for num in args[1:]:
                result /= float(num)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"

# Plugin Loader
class PluginLoader:
    def __init__(self, plugin_package):
        self.plugin_package = plugin_package
        self.commands = {}
        self.load_plugins()

    def load_plugins(self):
        package = importlib.import_module(self.plugin_package)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{self.plugin_package}.{module_name}")
            if hasattr(module, "COMMANDS"):
                self.commands.update(module.COMMANDS)

# Load Plugins
def load_dynamic_commands():
    plugin_loader = PluginLoader("plugins")
    return plugin_loader.commands

# Command Dictionary
commands = {
    "add": AddCommand(),
    "subtract": SubtractCommand(),
    "multiply": MultiplyCommand(),
    "divide": DivideCommand(),
}

# Integrate dynamic commands
commands.update(load_dynamic_commands())

# REPL Function
def repl():
    print("Welcome to the Command Pattern Calculator! Type 'menu' to see available commands, or 'exit' to quit.")
    while True:
        user_input = input("Enter command: ").strip().split()
        if not user_input:
            continue

        command_name = user_input[0]
        args = user_input[1:]

        if command_name == "exit":
            print("Exiting calculator. Goodbye!")
            break
        elif command_name == "menu":
            print("Available commands:", ", ".join(commands.keys()))
        elif command_name in commands:
            try:
                result = commands[command_name].execute(*args)
                print("Result:", result)
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid command. Type 'menu' to see available commands.")

if __name__ == "__main__":
    repl()

