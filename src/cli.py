from parser import parse_zsh_history
from analyzer import analyze_commands
from visualizer import create_bar_chart
from webserver import run_server

commands = parse_zsh_history()
frequencies = analyze_commands(commands)
top_commands = frequencies.most_common(10)
create_bar_chart(top_commands)

run_server()