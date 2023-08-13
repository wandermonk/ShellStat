import os
import matplotlib.pyplot as plt

def create_bar_chart(data, filename='chart.png'):
    static_folder = 'src/static'
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    plt.bar(*zip(*data))
    path = os.path.join(static_folder, filename)
    plt.savefig(path)