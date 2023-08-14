from collections import Counter
from collections import defaultdict


def analyze_commands(commands):
    return Counter(commands)


def analyze_security_risks(risks):
    return Counter(risks)


def analyze_commands_by_hour(commands_with_time):
    hourly_commands = {}
    for timestamp, command in commands_with_time:
        hour = timestamp.hour
        if hour not in hourly_commands:
            hourly_commands[hour] = []
        hourly_commands[hour].append(command)
    return hourly_commands


def analyze_length_and_complexity(analysis):
    results = defaultdict(list)
    for command, length, complexity in analysis:
        complexity_score = complexity['arguments'] + complexity['pipes'] + complexity['redirections']
        results[complexity_score].append((command, length))
    return results
