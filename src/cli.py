from file_reader import read_lines
from parser import parse_commands_with_time, parse_commands
from analyzer import analyze_commands, analyze_commands_by_hour
from visualizer import create_bar_chart, create_commands_by_hour
from webserver import run_server

lines = read_lines()
commands = parse_commands(lines)
commands_with_time = parse_commands_with_time(lines)

frequencies = analyze_commands(commands)
hourly_commands = analyze_commands_by_hour(commands_with_time)

top_commands = frequencies.most_common(10)

create_bar_chart(top_commands)
create_commands_by_hour(hourly_commands)

run_server()