import os
import matplotlib.pyplot as plt

static_folder = 'src/static'

def create_bar_chart(data, filename='frequency_chart.png'):
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    plt.bar(*zip(*data))
    path = os.path.join(static_folder, filename)
    plt.savefig(path)

def create_commands_by_hour(hourly_commands, filename='hourly_commands.png'):
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    plt.bar(hourly_commands.keys(), [len(commands) for commands in hourly_commands.values()])
    path = os.path.join(static_folder, filename)
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Commands')
    plt.title('Command Usage by Hour')
    plt.savefig(path)