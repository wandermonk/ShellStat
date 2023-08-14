import os


def get_history_file_path():
    if os.name == 'nt':
        return os.path.join(os.environ['APPDATA'], 'Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt')
    elif os.environ['SHELL'].endswith('zsh'):
        return os.path.expanduser("~/.zsh_history")
    elif os.environ['SHELL'].endswith('bash'):
        return os.path.expanduser("~/.bash_history")
    else:
        raise Exception("Unsupported shell")


def read_history_file():
    history_file_path = get_history_file_path()
    try:
        with open(history_file_path, "rb") as file:
            lines = file.read()
            lines = lines.decode("ISO-8859-1").split("\n")  # Adjust encoding as needed
            return lines
    except FileNotFoundError:
        print(f"History file not found at {history_file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the history file: {e}")
        return []
