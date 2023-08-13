import os

def parse_zsh_history():
    with open(os.path.expanduser("~/.zsh_history"), "rb") as file:
        lines = file.read()
        lines = lines.decode("ISO-8859-1").split("\n")
        
    commands = [line.split(';')[1].strip() if ';' in line else '' for line in lines]
    return commands