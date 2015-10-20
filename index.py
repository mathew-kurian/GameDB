#!/usr/bin/env python3

# pip3 install pyjade
# pip3 install Flask

# nohup ./index.py &

from flask import Flask, render_template
from flask.ext.compress import Compress

app = Flask(__name__, static_folder='public', static_url_path='/assets')
Compress(app)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.jade', assets='/assets/')


@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.jade', assets='/assets/')


@app.route('/games')
@app.route('/games.html')
def games():
    return render_template('models/games.jade', assets='/assets/')


@app.route('/releases')
@app.route('/releases.html')
def releases():
    return render_template('models/releases.jade', assets='/assets/')


@app.route('/publishers')
@app.route('/publishers.html')
def publishers():
    return render_template('models/publishers.jade', assets='/assets/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
