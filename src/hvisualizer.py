import os
import matplotlib
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Protocol, Tuple

matplotlib.use('Agg')
plt.ioff()

static_folder = 'src/static'


class Visualizer(Protocol):
    def visualize(self, data: Any, filename: str) -> None:
        ...

class BarChartVisualizer(Visualizer):
    def visualize(self, data: Dict[str, int], filename='frequency_chart.png') -> None:
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        plt.bar(*zip(*data.items()))
        path = os.path.join(static_folder, filename)
        plt.savefig(path)

class CommandsByHourVisualizer(Visualizer):
    def visualize(self, data: Dict[int, List[str]], filename='hourly_commands.png') -> None:
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        plt.bar(data.keys(), [len(commands) for commands in data.values()])
        path = os.path.join(static_folder, filename)
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Commands')
        plt.title('Command Usage by Hour')
        plt.savefig(path)

class LengthAndComplexityVisualizer(Visualizer):
    def visualize(self, data: Dict[int, List[Tuple[str, int]]], filename='length_and_complexity.png') -> None:
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        complexity_scores = []
        lengths = []
        for complexity_score, commands in data.items():
            for command, length in commands:
                complexity_scores.append(complexity_score)
                lengths.append(length)
        plt.scatter(complexity_scores, lengths)
        path = os.path.join(static_folder, filename)
        plt.xlabel('Complexity Score')
        plt.ylabel('Command Length')
        plt.title('Command Length vs Complexity')
        plt.savefig(path)

class SecurityRiskVisualizer(Visualizer):
    def visualize(self, data: Dict[str, int], filename='security_risks.png') -> None:
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
        labels, values = zip(*data.items())
        plt.barh(labels, values)
        path = os.path.join(static_folder, filename)
        plt.xlabel('Count')
        plt.ylabel('Risky Command')
        plt.title('Identified Security Risks')
        plt.savefig(path)
