import datetime
import re

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

def identify_security_risks(commands):
    risks = []
    risky_patterns = [
    r'rm\s+-rf', # Dangerous delete
    r'ssh\s+\S+@', # SSH command
    r'echo\s+[\'"].+[\'"]\s+>\s+/etc', # Overwriting system files
    r'sudo\s+.*', # Usage of sudo
    r'(password|api_key|token)=\S+', # Clear-text sensitive info
    r'(ftp|telnet)://\S+', # Insecure protocols
    r'(nmap|netstat)\s+.*', # Network scanning
    r'(wget|curl)\s+http://\S+', # Downloading files from HTTP
    #r'\.\s+/path/to/suspicious/script', # Running suspicious scripts
    r'eval\s+\$.*', # Eval with untrusted input
    r'(useradd|usermod|adduser)\s+.*', # User account changes
    r'gpasswd\s+-a\s+\S+\s+(admin|sudo|wheel)', # Adding users to privileged groups
    r'service\s+auditd\s+stop', # Stopping auditing
    r'(iptables|firewall-cmd)\s+.*', # Firewall changes
    r'dpkg\s+-i\s+.*', # Installing software packages
    #r'apt\s+remove\s+unattended-upgrades', # Disabling automatic updates
    r'(scp|rsync)\s+\S+\s+\S+@\S+:\S+' # Data transfers
    # Add more patterns as needed
    ]
    for command in commands:
        for pattern in risky_patterns:
            if re.search(pattern, command):
                risks.append(command)
    return risks