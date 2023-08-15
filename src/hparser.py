from typing import List, Dict, Tuple, Any, Protocol, Optional, Pattern
import datetime
import re

class Parser(Protocol):
    def parse(self, data: Any, patterns: Optional[Dict[str, str]] = None) -> Any:
        ...

###
#  Split Pattern for new line "\n"
###
class CommandParser(Parser):
    def parse(self, data: str) -> List[str]:
        if len(data) == 0:
            return []
        commands = [line.split(';')[1].strip() if ';' in line else '' for line in data]
        return commands

###
#  Split Pattern for time ";"
#  Split Pattern for time parts ":"
###
class CommandWithTimeParser(Parser):
    def parse(self, data: str, patterns: Optional[Dict[str, str]] = None) -> List[Tuple[Any, str]]:
        if patterns:
            command_separator = patterns.get('command_split', ';')
            timestamp_separator = patterns.get('timestamp_split', ':')
        else:
            command_separator = ';'
            timestamp_separator = ':'
        
        if not data:
            return []

        commands_with_time = []
        for line in data:
            parts = line.split(command_separator)
            if len(parts) > 1:
                timestamp_parts = parts[0].strip().split(timestamp_separator)
                if len(timestamp_parts) > 1:
                    timestamp = timestamp_parts[1]  # This assumes the timestamp is the second part
                    command = parts[1].strip()
                    timestamp = datetime.datetime.fromtimestamp(int(timestamp))
                    commands_with_time.append((timestamp, command))
                else:
                    commands_with_time.append((datetime.datetime.fromtimestamp(int(timestamp_parts[0])), parts[1].strip()))
        return commands_with_time


###
# Complexity Pattern for arguments " "
# Complexity Pattern for pipes "|"
# Complexity Pattern for redirections "<" and ">"
###
class CommandLengthAndComplexityParser(Parser):
    def parse(self, data: str, patterns: Optional[Dict[str, str]] = None) -> List[Tuple[str, int, Dict[str, int]]]:
        # If patterns are provided, use them, else use default string separators
        argument_sep = patterns.get('arguments', ' ') if patterns else ' '
        pipe_sep = patterns.get('pipes', '|') if patterns else '|'
        redirection_left = patterns.get('redirections_left', '<') if patterns else '<'
        redirection_right = patterns.get('redirections_right', '>') if patterns else '>'
        
        lines = []
        for command in data:  # Assuming data is multiline string and needs to be split
            length = len(command)
            complexity = {
                'arguments': command.count(argument_sep),
                'pipes': command.count(pipe_sep),
                'redirections': command.count(redirection_left) + command.count(redirection_right)
            }
            lines.append((command, length, complexity))
        return lines

###
# Security Patterns for risky commands
#  re.compile(r'\b(rm\s+\-rf.*)'),
#  re.compile(r'\b(curl\s+\|.*sh)'),
#  re.compile(r'wget.*\|.*sh'),
#  re.compile(r'\b(disable\-security\-feature\b)'),
#  re.compile(r'rm\s+-rf'),
#  re.compile(r'ssh\s+\S+@'),
#  re.compile(r'echo\s+[\'"].+[\'"]\s+>\s+/etc'),
#  re.compile(r'sudo\s+.*'),
#  re.compile(r'(password|api_key|token)=\S+'),
#  re.compile(r'(ftp|telnet)://\S+'),
#  re.compile(r'(nmap|netstat)\s+.*'),
#  re.compile(r'(wget|curl)\s+http://\S+'),
#  re.compile(r'eval\s+\$.*'),
#  re.compile(r'(useradd|usermod|adduser)\s+.*'),
#  re.compile(r'gpasswd\s+-a\s+\S+\s+(admin|sudo|wheel)'),
#  re.compile(r'service\s+auditd\s+stop'),
#  re.compile(r'(iptables|firewall-cmd)\s+.*'),
#  re.compile(r'dpkg\s+-i\s+.*'),
#  re.compile(r'(scp|rsync)\s+\S+\s+\S+@\S+:\S+'),
###
class CommandRiskParser(Parser):
    DEFAULT_RISK_PATTERNS = [
        re.compile(r'\b(rm\s+\-rf.*)'),
        re.compile(r'\b(curl\s+\|.*sh)'),
        re.compile(r'\b(rm\s+\-rf.*)'),
        re.compile(r'\b(curl\s+\|.*sh)'),
        re.compile(r'wget.*\|.*sh'),
        re.compile(r'\b(disable\-security\-feature\b)'),
        re.compile(r'rm\s+-rf'),
        re.compile(r'ssh\s+\S+@'),
        re.compile(r'echo\s+[\'"].+[\'"]\s+>\s+/etc'),
        re.compile(r'sudo\s+.*'),
        re.compile(r'(password|api_key|token)=\S+'),
        re.compile(r'(ftp|telnet)://\S+'),
        re.compile(r'(nmap|netstat)\s+.*'),
        re.compile(r'(wget|curl)\s+http://\S+'),
        re.compile(r'eval\s+\$.*'),
        re.compile(r'(useradd|usermod|adduser)\s+.*'),
        re.compile(r'gpasswd\s+-a\s+\S+\s+(admin|sudo|wheel)'),
        re.compile(r'service\s+auditd\s+stop'),
        re.compile(r'(iptables|firewall-cmd)\s+.*'),
        re.compile(r'dpkg\s+-i\s+.*'),
        re.compile(r'(scp|rsync)\s+\S+\s+\S+@\S+:\S+'),
    ]

    def parse(self, data: str, patterns: Optional[List[Pattern]] = None) -> List[str]:
        if not patterns:
            patterns = self.DEFAULT_RISK_PATTERNS
            
        risky_commands = []
        
        # We're assuming data contains multiple commands separated by newlines
        for command in data:
            for pattern in patterns:
                if pattern.search(command):
                    risky_commands.append(command)
                    break  # only add a command once, even if it matches multiple patterns
        
        return risky_commands