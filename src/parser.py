import datetime

def parse_commands(lines):
    commands = [line.split(';')[1].strip() if ';' in line else '' for line in lines]
    return commands

def parse_commands_with_time(lines):
    commands_with_time = []
    for line in lines:
        parts = line.split(";")
        if len(parts) > 1:
            timestamp_parts = parts[0].strip().split(':')
            if len(timestamp_parts) > 1:
                timestamp = timestamp_parts[1]  # This assumes the timestamp is the second part
                command = parts[1].strip()
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                commands_with_time.append((timestamp, command))
    return commands_with_time

def command_length_and_complexity(commands):
    analysis = []
    for command in commands:
        length = len(command)
        complexity = {
            'arguments': command.count(' '),
            'pipes': command.count('|'),
            'redirections': command.count('>') + command.count('<')
        }
        analysis.append((command, length, complexity))
    return analysis