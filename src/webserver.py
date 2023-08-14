from flask import Flask, render_template_string, url_for

app = Flask(__name__)


@app.route('/')
def index():
    image_url = url_for('static', filename='chart.png')
    return render_template_string("<img src='{{ iamge_url }}'>", image_url=image_url)


def run_server():
    app.run(debug=True)
