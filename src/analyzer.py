from collections import Counter

def analyze_commands(commands):
    return Counter(commands)

def analyze_commands_by_hour(commands_with_time):
    hourly_commands = {}
    for timestamp, command in commands_with_time:
        hour = timestamp.hour
        if hour not in hourly_commands:
            hourly_commands[hour] = []
        hourly_commands[hour].append(command)
    return hourly_commands