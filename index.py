#!/usr/bin/env python3
import os
import subprocess
import time
import argparse
import json
import flask
from flask import Flask, render_template, make_response, request, Response
import flask
from flask.ext.compress import Compress
import pysolr as pysolr
from sqlalchemy.exc import InvalidRequestError
from solr import normalize_results

from http.client import HTTPConnection

from db import *

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=int(os.environ.get("PORT", 80)))
parser.add_argument("-d", "--debug", action='store_true')
args = parser.parse_args()

app = Flask(__name__, static_folder='public', static_url_path='/assets')
Compress(app)

solr = pysolr.Solr('http://104.130.23.111:8983/solr/4playdb', timeout=10)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = args.debug

# open session
session = get_session(echo=False)


# run bash command
def run_command(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break


# send feedback on status of API request
def send_api_response(func, tables, table):
    start_time = time.time()
    res = {'status': 0, 'message': 'Success', 'results': []}

    if table in tables:
        try:
            doc = func(tables[table])
            if doc:
                res['results'] += doc if isinstance(doc, list) else [doc]
            else:
                res['message'] = 'ID not found'
        except InvalidRequestError as e:
            global session
            session.close()
            session = get_session(echo=False)
            return send_api_response(func, tables, table)
        except Exception as e:
            res['status'] = 1
            res['message'] = str(e)
            print(e)
    else:
        res['status'] = 1
        res['message'] = 'Table not found'

    res['time'] = "%.2fs" % (time.time() - start_time)
    return Response(to_json(res), mimetype='application/json', status=404 if res['status'] else 200)


# enable API get
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


# enable API search
# index specifies which 10 to get, using zero-based indexing
# Ex. index = 0 means first 10, index = 1 means 11 - 20
@app.route('/api/search')
@app.route('/api/search/')
def api_search():
    start_time = time.time()
    res = {'status': 0, 'message': 'Success', 'results': []}

    q = request.args.get('q', default=None, type=str)

    if not q:
        res['status'] = 1
        res['message'] = 'No query'
    else:

        offset = request.args.get('offset', default=0, type=int)
        limit = max(min(request.args.get('limit', default=25, type=int), 25), 0)
        results = solr.search({})

        try:

            def query(mode, mult=1):
                sq = []
                keywords = ' '.join(q.split()).split(' ')

                for k in keywords:
                    if len(k) < 3:  # test and remove the count as needed
                        continue
                    sq += ['(name:(' + k + ') OR deck:(' + k + '))']

                op = '(' + (' ' + mode + ' ').join(sq) + ')'

                res = solr.search(op, **{
                    'rows': limit,
                    'start': limit * offset,
                    'fl': 'id,name,deck,description,entity',
                    'hl': 'true',
                    'hl.fl': 'name deck description',
                    'hl.fragsize': 30,
                    'hl.snippets': '5',
                    'hl.mergeContiguous': 'true',
                    'hl.simple.pre': '<span class="highlight">',
                    'hl.simple.post': '</span>',
                    'hl.highlightMultiTerm': 'true'
                })

                dist = 1
                for r in res:
                    r['__mode__'] = mode
                    r['__dist__'] = dist * mult  # lower the distance, better the result
                    r['__highlighting__'] = {}
                    if r['id'] in res.highlighting:
                        r['__highlighting__'] = res.highlighting[r['id']]
                    dist += 1

                return res

            def mapify(a, k):
                m = {}
                for i in a:
                    m[i[k]] = i
                return m

            def listify(a):
                l = []
                for i in a:
                    l += [a[i]]
                return l

            def assign(a, b):
                for i in b:
                    a[i] = b[i]
                return a

            results = listify(assign(mapify(query('OR', 25), 'id'), mapify(query('AND'), 'id')))
            results.sort(key=lambda x: x['__dist__'])

            filtered = []
            for result in results:
                hasdesc = None
                highlighting = result['__highlighting__']
                hasdesc = 'description' in highlighting
                if len(highlighting) == 0:
                    continue
                for key in highlighting:
                    result[key] = '...'.join(highlighting[key])
                for key in result:
                    if type(result[key]) == list:
                        result[key] = result[key][0]
                if not hasdesc and 'description' in result:
                    del result['description']
                filtered += [result]

            results = filtered

            for l in results:
                t = {'company': Company, 'game': Game, 'platform': Platform}[l['entity']]
                doc = session.query(t).get(l['id'])
                l['images'] = to_dict(doc.images)

            res['results'] = [to_dict(r) for r in results]

        except InvalidRequestError as e:
            global session
            session.close()
            session = get_session(echo=False)
            return api_search()
        except Exception as e:
            res['status'] = 1
            res['message'] = str(e)
            print(e)

    res['time'] = "%.2fs" % (time.time() - start_time)
    return Response(to_json(res), mimetype='application/json', status=404 if res['status'] else 200)


# run unit tests
@app.route('/run-tests')
def tests():
    res = ''
    path = os.path.dirname(os.path.realpath(__file__))
    for i in run_command(('python3 ' + path + '/tests.py').split()):
        res += i.decode("utf-8")

    return Response(res, mimetype='text/plain')


# render html template
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('client.jade')


# add headers
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes. Ensure all
    responses have the CORS headers. This ensures any failures are also accessible
    by the client.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=60000000'
    response.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    response.headers['Access-Control-Allow-Headers'] = flask.request.headers.get(
        'Access-Control-Request-Headers', 'Authorization')
    # set low for debugging
    if app.debug:
        response.headers['Access-Control-Max-Age'] = '1'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
