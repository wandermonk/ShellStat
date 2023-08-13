import pytest
from src.parser import parse_commands, parse_commands_with_time, command_length_and_complexity, identify_security_risks
from datetime import datetime

def test_parse_commands():
    assert parse_commands([";command1", "1587587568:command2;", ";command3"]) == ["command1", "", "command3"]
    assert parse_commands(["no_semicolon"]) == ['']
    assert parse_commands([]) == []

def test_parse_commands_with_time():
    assert parse_commands_with_time(["1587587568;command1"]) == [(datetime.fromtimestamp(int(1587587568)), "command1")]
    assert parse_commands_with_time(["no_semicolon"]) == []
    assert parse_commands_with_time([]) == []

def test_command_length_and_complexity():
    assert command_length_and_complexity(["ls"]) == [("ls", 2, {'arguments': 0, 'pipes': 0, 'redirections': 0})]
    assert command_length_and_complexity(["ls -l"]) == [("ls -l", 5, {'arguments': 1, 'pipes': 0, 'redirections': 0})]
    assert command_length_and_complexity(["cat | grep test"]) == [("cat | grep test", 15, {'arguments': 3, 'pipes': 1, 'redirections': 0})]
    assert command_length_and_complexity(["echo 'hello' > file"]) == [("echo 'hello' > file", 19, {'arguments': 3, 'pipes': 0, 'redirections': 1})]

def test_identify_security_risks():
    commands = [
        "rm -rf /",
        "ssh user@host",
        "echo 'password' > /etc/passwd",
        "ls -l",
        "eval $dangerous_command",
        "service auditd stop",
        "rsync /local/file user@host:/remote/file"
    ]
    expected_result = [
        "rm -rf /",
        "ssh user@host",
        "echo 'password' > /etc/passwd",
        "eval $dangerous_command",
        "service auditd stop",
        "rsync /local/file user@host:/remote/file"
    ]
    assert identify_security_risks(commands) == expected_result
