from collections import Counter
from src.analyzer import analyze_commands, analyze_security_risks, analyze_commands_by_hour, analyze_length_and_complexity

import datetime

def test_analyze_commands():
    commands = ['ls', 'pwd', 'ls', 'ls']
    assert analyze_commands(commands) == Counter({'ls': 3, 'pwd': 1})

def test_analyze_security_risks():
    risks = ['ssh user@', 'rm -rf', 'ssh user@']
    assert analyze_security_risks(risks) == Counter({'ssh user@': 2, 'rm -rf': 1})

def test_analyze_commands_by_hour():
    commands_with_time = [(datetime.datetime(2021, 6, 1, 12, 0), 'ls'), (datetime.datetime(2021, 6, 1, 12, 30), 'pwd')]
    assert analyze_commands_by_hour(commands_with_time) == {12: ['ls', 'pwd']}

def test_analyze_length_and_complexity():
    analysis = [('ls', 2, {'arguments': 0, 'pipes': 0, 'redirections': 0}), ('ls -l', 4, {'arguments': 1, 'pipes': 0, 'redirections': 0})]
    assert analyze_length_and_complexity(analysis) == {0: [('ls', 2)], 1: [('ls -l', 4)]}
