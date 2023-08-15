from flask import Flask, render_template_string, url_for
from db import RocksDBConnection
import os

from file_reader import get_history_file_path, get_or_create_metrics_file

app = Flask(__name__)


@app.route('/')
def index():
    image_url = url_for('static', filename='chart.png')
    return render_template_string("<img src='{{ iamge_url }}'>", image_url=image_url)

@app.route('/metrics')
def metrics():
    _db = RocksDBConnection._instance.db
    return render_template_string("""
    <html>
        <head>
            <title>Metrics</title>
        </head>
        <body>
            <h1>Metrics</h1>
            <h2>Total Commands</h2>
            <p>{{ total_commands }}</p>
            <h2>Commands By Hour</h2>
            <p>{{ commands_by_hour }}</p>
            <h2>Complexity</h2>
            <p>{{ complexity }}</p>
            <h2>Command Length</h2>
            <p>{{ command_length }}</p>
            <h2>Security Risk</h2>
            <p>{{ security_risk }}</p>
        </body>
    </html>
    """, 
    total_commands=_db.get('total_commands', "N/A"),
    commands_by_hour=_db.get('commands_by_hour', "N/A"),
    complexity=_db.get('complexity', "N/A"),
    command_length=_db.get('command_length', "N/A"),
    security_risk=_db.get('security_risk', "N/A")
    )
