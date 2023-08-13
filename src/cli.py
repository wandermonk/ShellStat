from file_reader import read_lines
from parser import parse_commands_with_time, parse_commands, command_length_and_complexity
from analyzer import analyze_commands, analyze_commands_by_hour, analyze_length_and_complexity
from visualizer import create_bar_chart, create_commands_by_hour, visualize_length_and_complexity
from webserver import run_server

lines = read_lines()
commands = parse_commands(lines)
commands_with_time = parse_commands_with_time(lines)

frequencies = analyze_commands(commands)
hourly_commands = analyze_commands_by_hour(commands_with_time)
command_length = command_length_and_complexity(commands)

top_commands = frequencies.most_common(10)
length_and_complexity = analyze_length_and_complexity(command_length)

create_bar_chart(top_commands)
create_commands_by_hour(hourly_commands)
visualize_length_and_complexity(length_and_complexity)

run_server()