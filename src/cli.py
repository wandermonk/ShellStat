import os
import time
from watchdog.observers import Observer
from file_reader import FileChangeHandler
from webserver import app

from threading import Thread
from file_reader import get_or_create_snapshot_file, get_last_committed_offset, get_history_file_path, get_or_create_metrics_file
from hparser import CommandParser, CommandWithTimeParser, CommandLengthAndComplexityParser, CommandRiskParser
from hanalyzer import CommandAnalyzer, CommandsByHourAnalyzer, ComplexityAnalyzer, CommandLengthAnalyzer, SecurityRiskAnalyzer

from db import RocksDBConnection

def watch_history(history_file_path, offset, metrics_file):
    # initialize parsers
    command_parser = CommandParser()
    risk_parser = CommandRiskParser()
    command_with_time_parser = CommandWithTimeParser()
    command_length_and_complexity_parser = CommandLengthAndComplexityParser()
    # initialize analyzers
    command_analyzer = CommandAnalyzer()
    commands_by_hour_analyzer = CommandsByHourAnalyzer()
    complexity_analyzer = ComplexityAnalyzer()
    command_length_analyzer = CommandLengthAnalyzer()
    risk_analyzer = SecurityRiskAnalyzer()  

    handler = FileChangeHandler(
        history_file_path, 
        offset, 
        RocksDBConnection.__new__(RocksDBConnection, metrics_file).db,
        parsers=[command_parser, command_with_time_parser, command_length_and_complexity_parser, risk_parser],
        analyzers=[command_analyzer, commands_by_hour_analyzer, complexity_analyzer, command_length_analyzer, risk_analyzer],
        )
    observer = Observer()
    observer.schedule(handler, os.path.dirname(history_file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    return handler.offset



def run_server():
    app.run(debug=True, use_reloader=False, port=5000)


def main():
    server_thread = Thread(target=run_server)
    server_thread.start()

    snapshot_file_path = get_or_create_snapshot_file(os.path.dirname(get_history_file_path()), os.path.join(os.path.dirname(get_history_file_path()), '.history_snapshot'))
    last_committed_offset = get_last_committed_offset(snapshot_file_path)
    history_file = get_history_file_path()
    metrics_file = get_or_create_metrics_file(history_file)

    print(f"Reading history file: {history_file} from offset: {last_committed_offset} \n")
    try:
        offset = watch_history(history_file, last_committed_offset, metrics_file)
    except KeyboardInterrupt:
        offset = last_committed_offset
    print(f"Writing offset: {offset} to snapshot file: {snapshot_file_path}")
    with open(snapshot_file_path, 'w') as snapshot_file:
        snapshot_file.write(str(offset))
    server_thread.join()
    RocksDBConnection.db.close()
    

if __name__ == "__main__":
    main()