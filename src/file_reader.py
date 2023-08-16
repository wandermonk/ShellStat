import os
from watchdog.events import FileSystemEventHandler
from hanalyzer import CommandAnalyzer, CommandsByHourAnalyzer, ComplexityAnalyzer, CommandLengthAnalyzer, SecurityRiskAnalyzer
from hvisualizer import BarChartVisualizer, CommandsByHourVisualizer, LengthAndComplexityVisualizer, SecurityRiskVisualizer

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filepath, offset, db, parsers=[], analyzers=[]):
        self.filepath = filepath
        self.offset = offset
        self.parsers = parsers
        self.analyzers = analyzers

    def on_modified(self, event):
        if event.src_path == self.filepath:
            with open(self.filepath, 'rb') as file:
                file.seek(self.offset) # Seek to the last committed offset
                new_lines = file.read()
                new_lines_decoded = new_lines.decode("ISO-8859-1").split("\n")
                parsed_data_list = []
                for parser in self.parsers:
                    parsed_data = parser.parse(new_lines_decoded)
                    parsed_data_list.append(parsed_data)

                for data, analyzer in zip(parsed_data_list, self.analyzers):
                    if isinstance(analyzer, CommandAnalyzer):
                        BarChartVisualizer().visualize(analyzer.analyze(data))
                    elif isinstance(analyzer, CommandsByHourAnalyzer):
                        CommandsByHourVisualizer().visualize(analyzer.analyze(data))
                    elif isinstance(analyzer, ComplexityAnalyzer):
                        LengthAndComplexityVisualizer().visualize(analyzer.analyze(data))
                    elif isinstance(analyzer, CommandLengthAnalyzer):
                        LengthAndComplexityVisualizer().visualize(analyzer.analyze(data))
                    elif isinstance(analyzer, SecurityRiskAnalyzer):
                        SecurityRiskVisualizer().visualize(analyzer.analyze(data))
                    else:
                        raise Exception("Unknown analyzer type")
                # Process the decoded lines for generating insights.
                self.offset = file.tell() # Update the offset

# TODO: Make this configurable
def get_or_create_snapshot_file(base_dir, snapshot_file_path):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    if not os.path.exists(snapshot_file_path):
        open(snapshot_file_path, 'w').close()
    return snapshot_file_path

def get_last_committed_offset(snapshot_file_path):
    try:
        with open(snapshot_file_path, 'r') as snapshot_file:
            return int(snapshot_file.read())
    except FileNotFoundError:
        print(f"Snapshot file not found at {snapshot_file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred while reading the snapshot file: {e}")
        return 0

# This should not only get the filepath but also last committed offset
# The offset represents the last line that was committed to the snapshot file
# This determined from which position the file needs to be seeked
def get_history_file_path():
    if os.name == 'nt':
        return os.path.join(os.environ['APPDATA'], 'Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt')
    elif os.environ['SHELL'].endswith('zsh'):
        return os.path.expanduser("~/.zsh_history")
    elif os.environ['SHELL'].endswith('bash'):
        return os.path.expanduser("~/.bash_history")
    else:
        raise Exception("Unsupported shell")
    
def get_or_create_metrics_file(history_file):
    metrics_file = os.path.join(os.path.dirname(history_file), '.metrics')
    if not os.path.exists(metrics_file):
        open(metrics_file, 'w').close()
    return metrics_file