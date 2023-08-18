from flask import Flask, render_template_string, url_for
import os
from db import TimeseriesDB

app = Flask(__name__)


@app.route('/')
def index():
    image_url = url_for('static', filename='chart.png')
    return render_template_string("<img src='{{ iamge_url }}'>", image_url=image_url)

@app.route('/metrics')
def metrics():
    db = TimeseriesDB()
    metrics = db.get_metrics_metadata()
    print(metrics)
    return render_template_string("""
    <table>
        <tr>
            <th>Metric Name</th>
            <th>Metric Value</th>
        </tr>
        {% for metric in metrics %}
            <tr>
                <td>{{ metric[0] }}</td>
                <td>{{ metric[1] }}</td>
            </tr>
        {% endfor %}
    </table>
    """, metrics=metrics)