#!/usr/bin/env python3
import os
import subprocess
import time
import argparse

from flask import Flask, render_template, make_response, request, Response
from flask.ext.compress import Compress
from flask.ext.cors import CORS

from db import *

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 80)))
parser.add_argument("-d", "--debug", action='store_true')
args = parser.parse_args()

app = Flask(__name__, static_folder='public', static_url_path='/assets')
Compress(app)
CORS(app)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = args.debug

#open session
session = get_session(echo=False)

#run bash command
def run_command(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

#send feedback on status of API request
def send_api_response(func, tables, table):
    start_time = time.time()
    res = {'status': 1, 'message': 'Success', 'results': []}

    if table in tables:
        try:
            doc = func(tables[table])
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
    return Response(to_json(res), mimetype='application/json', status=404 if res['status'] else 200)

#enable API
@app.route('/api/<string:table>')
@app.route('/api/<string:table>/')
@app.route('/api/<string:table>/<int:id>')
def api(table, id=-1):
    if id == -1:
        offset = request.args.get('offset', default=0, type=int)
        limit = max(min(request.args.get('limit', default=25, type=int), 25), 0)
        return send_api_response(
            lambda t: [dict((m, getattr(i, m)) for m in ('id', 'name', 'deck', 'images')) for i in
                       session.query(t).limit(limit).offset(offset).all()],
            {'companies': Company, 'games': Game, 'platforms': Platform}, table)
    return send_api_response(lambda t: session.query(t).get(id),
                             {'company': Company, 'game': Game, 'platform': Platform}, table)

#run unit tests
@app.route('/run-tests')
def tests():
    res = ''
    path = os.path.dirname(os.path.realpath(__file__))
    for i in run_command(('python3 ' + path + '/tests.py').split()):
        res += i.decode("utf-8")

    return Response(res, mimetype='text/plain')

#render html template
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('client.jade')

#add headers
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=60000000'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
