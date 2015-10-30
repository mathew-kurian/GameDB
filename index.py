#!/usr/bin/env python3

import time

from flask import Flask, render_template, abort, make_response, request
from flask.ext.compress import Compress

from db import *

app = Flask(__name__, static_folder='public', static_url_path='/assets')
Compress(app)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

session = get_session(echo=False)

with open('scripts/giantbomb/connected/games.json') as f:
    games_db = json.load(f)

with open('scripts/giantbomb/connected/companies.json') as f:
    companies_db = json.load(f)

with open('scripts/giantbomb/connected/platforms.json') as f:
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


def send_api_response(func, table):
    start_time = time.time()
    res = {'status': 1, 'message': 'Success', 'results': []}

    if table:
        try:
            doc = func(table)
            if doc:
                res['status'] = 0
                res['results'] += doc if isinstance(doc, list) else [doc]
            else:
                res['message'] = 'ID not found'
        except Exception as e:
            res['message'] = str(e)
            print(e)
    else:
        res['message'] = 'Table not found'

    res['time'] = "%.2fs" % (time.time() - start_time)
    res = make_response(to_json(res), 404 if res['status'] else 200)
    res.mimetype = 'application/json'
    return res


def p(a):
    print(a)
    return a


@app.route('/api/<string:table>')
@app.route('/api/<string:table>/')
@app.route('/api/<string:table>/<int:id>')
def api(table, id=-1):
    if id == -1:
        offset = request.args.get('offset', default=0, type=int)
        limit = max(min(request.args.get('limit', default=25, type=int), 25), 0)
        return send_api_response(lambda t: session.query(t).limit(limit).offset(offset).all(),
                                 {'companies': Company, 'games': Game, 'platforms': Platform}[table])
    return send_api_response(lambda t: session.query(t).get(id),
                             {'company': Company, 'game': Game, 'platform': Platform}[table])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
