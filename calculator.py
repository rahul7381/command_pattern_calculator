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
        return sum(float(num) for num in args)

class SubtractCommand(Command):
    def execute(self, *args):
        numbers = list(map(float, args))
        return numbers[0] - sum(numbers[1:])

class MultiplyCommand(Command):
    def execute(self, *args):
        result = 1.0
        for num in map(float, args):
            result *= num
        return result

class DivideCommand(Command):
    def execute(self, *args):
        try:
            numbers = list(map(float, args))
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    return "Error: Division by zero"
                result /= num
            return result
        except (ValueError, IndexError):
            return "Error: Invalid input"

# Plugin Loader
class PluginLoader:
    def __init__(self, plugin_package):
        self.plugin_package = plugin_package
        self.commands = {}
        self.load_plugins()

    def load_plugins(self):
        """Dynamically loads plugins from the plugins directory."""
        try:
            package = importlib.import_module(self.plugin_package)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{self.plugin_package}.{module_name}")
                if hasattr(module, "COMMANDS"):
                    self.commands.update(module.COMMANDS)
        except ModuleNotFoundError:
            print(f"Error: Plugin package '{self.plugin_package}' not found.")
        except Exception as e:
            print(f"Error loading plugins: {e}")

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
        try:
            user_input = input("Enter command: ").strip().split()
            if not user_input:
                continue

            command_name = user_input[0]
            args = user_input[1:]

            if command_name == "exit":
                print("Exiting calculator. Goodbye!")
                break
            elif command_name == "menu":
                print("Available commands:", ", ".join(sorted(commands.keys())))
            elif command_name in commands:
                print("Result:", commands[command_name].execute(*args))
            else:
                print("Invalid command. Type 'menu' to see available commands.")
        except KeyboardInterrupt:
            print("\nExiting calculator. Goodbye!")
            break

if __name__ == "__main__":
    repl()

