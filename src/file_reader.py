import os

def read_lines():
    with open(os.path.expanduser("~/.zsh_history"), "rb") as file:
        lines = file.read()
        lines = lines.decode("ISO-8859-1").split("\n")
        return lines