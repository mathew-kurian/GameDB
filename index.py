#!/usr/bin/env python3

# pip3 install pyjade
# pip3 install Flask

# nohup ./index.py &

from flask import Flask, render_template, abort
from flask.ext.compress import Compress

import json

app = Flask(__name__, static_folder='public', static_url_path='/assets')
Compress(app)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

with open('scripts/giantbomb/db/games.connected.json') as f:
    games_db = json.load(f)

with open('scripts/giantbomb/db/companies.connected.json') as f:
    companies_db = json.load(f)

with open('scripts/giantbomb/db/platforms.connected.json') as f:
    platforms_db = json.load(f)

def router(db, model, id=-1):
    if id == -1: return render_template('models/' + model + '.jade', assets='/assets/', props=json.dumps(db))
    for i in db:
        if i['id'] == id:
            i['mode'] = model;
            return render_template('records/' + model + '.jade', assets='/assets/', props=json.dumps(i))
    abort(404)


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
@app.route('/games/<int:id>')
@app.route('/games.html')
def games(id=-1):
    return router(games_db, 'games', id)


@app.route('/platforms')
@app.route('/platforms/<int:id>')
@app.route('/platforms.html')
def platforms(id=-1):
    return router(platforms_db, 'platforms', id)


@app.route('/companies')
@app.route('/companies/<int:id>')
@app.route('/companies.html')
def companies(id=-1):
    return router(companies_db, 'companies', id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
