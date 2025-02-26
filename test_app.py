import pytest
from calculator import commands, repl, PluginLoader
from io import StringIO
import sys

# Test basic calculator commands
@pytest.mark.parametrize("command, inputs, expected_output", [
    ("add", ["5", "10"], "15.0"),
    ("subtract", ["10", "3"], "7.0"),
    ("multiply", ["2", "4"], "8.0"),
    ("divide", ["8", "2"], "4.0"),
])
def test_calculator_commands(command, inputs, expected_output):
    """Test basic calculator operations."""
    result = commands[command].execute(*inputs)
    assert str(result) == expected_output

# Test divide by zero
def test_division_by_zero():
    """Test division by zero error handling."""
    result = commands["divide"].execute("10", "0")
    assert result == "Error: Division by zero"

# Test invalid input for all commands
@pytest.mark.parametrize("command, inputs", [
    ("add", ["a", "b"]),
    ("subtract", ["x", "5"]),
    ("multiply", ["@", "#"]),
    ("divide", ["8", "0"]),
])
def test_invalid_inputs(command, inputs):
    """Test calculator with invalid inputs."""
    try:
        result = commands[command].execute(*inputs)
        assert isinstance(result, str)  # Should return an error message
    except ValueError:
        assert True  # Expected failure

# Test the REPL handling known commands
def test_repl_known_command(monkeypatch, capsys):
    """Test that REPL correctly processes known commands."""
    inputs = iter(["add 3 7", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    sys.stdout = StringIO()
    repl()
    sys.stdout.seek(0)
    output = sys.stdout.read()

    assert "Result: 10.0" in output
    assert "Exiting calculator. Goodbye!" in output

# Test the REPL handling unknown commands
def test_repl_unknown_command(monkeypatch, capsys):
    """Test that REPL correctly handles unknown commands."""
    inputs = iter(["unknown_command", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    sys.stdout = StringIO()
    repl()
    sys.stdout.seek(0)
    output = sys.stdout.read()

    assert "Invalid command. Type 'menu' to see available commands." in output
    assert "Exiting calculator. Goodbye!" in output

# Test the REPL menu command
def test_repl_menu_command(monkeypatch, capsys):
    """Test if the 'menu' command displays available commands in REPL."""
    inputs = iter(["menu", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    sys.stdout = StringIO()
    repl()
    sys.stdout.seek(0)
    output = sys.stdout.read()

    assert "Available commands:" in output
    assert "add" in output
    assert "subtract" in output
    assert "multiply" in output
    assert "divide" in output

# Test empty input in REPL
def test_repl_empty_input(monkeypatch, capsys):
    """Test how REPL handles when user presses enter without input."""
    inputs = iter(["", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    sys.stdout = StringIO()
    repl()
    sys.stdout.seek(0)
    output = sys.stdout.read()

    assert "Exiting calculator. Goodbye!" in output

# Test keyboard interrupt in REPL
def test_repl_keyboard_interrupt(monkeypatch, capsys):
    """Test REPL handling of keyboard interruption (CTRL + C)."""

    # Make input() raise KeyboardInterrupt when called
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))

    sys.stdout = StringIO()
    try:
        repl()
    except SystemExit:
        pass  # Expect the REPL to exit when KeyboardInterrupt occurs

    sys.stdout.seek(0)
    output = sys.stdout.read()

    assert "Exiting calculator. Goodbye!" in output

# Test PluginLoader when the plugin directory is missing
def test_plugin_loader_missing_directory(capfd):
    """Test PluginLoader when the plugin directory does not exist."""
    loader = PluginLoader("fake_plugins")
    captured = capfd.readouterr()
    assert "Error: Plugin package 'fake_plugins' not found." in captured.out

# Test PluginLoader when no commands are found
def test_plugin_loader_no_commands(capfd, monkeypatch):
    """Test PluginLoader when no valid commands exist in plugins."""

    monkeypatch.setattr("calculator.load_dynamic_commands", lambda: {})

    loader = PluginLoader("plugins_empty")  # Fake empty plugin folder
    captured = capfd.readouterr()

    assert captured.out.strip() == "" or "Error: Plugin package 'plugins_empty' not found." in captured.out

# Test PluginLoader exception handling for a broken plugin
def test_plugin_loader_broken_plugin(monkeypatch):
    """Test PluginLoader when a plugin fails to load."""

    def mock_import_error(*args, **kwargs):
        raise ImportError("Mocked import error")

    monkeypatch.setattr("importlib.import_module", mock_import_error)

    try:
        loader = PluginLoader("plugins")
    except ImportError as e:
        assert "Mocked import error" in str(e)

