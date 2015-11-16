#!/usr/bin/env python3
import os
import subprocess
import time
import argparse
import json

from flask import Flask, render_template, make_response, request, Response
import flask
from flask.ext.compress import Compress
from flask.ext.cors import CORS

from http.client import HTTPConnection

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

#enable API get
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

#enable API search
#index specifies which 10 to get, using zero-based indexing
#Ex. index = 0 means first 10, index = 1 means 11 - 20
@app.route('/api/search/<string:name>')
@app.route('/api/search/<string:name>/<int:index>')
def api_search(name, index = 0):
    #res object for response
    res = {'status': 1, 'message': 'Success', 'results': [], 'counted' : 0}

    #make a request to solr and read it
    connect = HTTPConnection('0.0.0.0:8983')
    connect.request('GET', '/solr/gettingstarted_shard1_replica2/select?q=' + name +'&wt=json&indent=true&fl=name,id,deck,description,country,online_support&start=' + str(index * 10))
    read = connect.getresponse()
    json_data = read.read()
    connect.close()

    #need to handle and display errors
    try:
        #convert json_data string to dict
        search_dict = json.loads(str(json_data.decode('utf-8')))
        counted = 0
        x = -1

        #get results for output, with at most 10
        while counted < 10:
            x += 1
            #break if not enough results
            if len(search_dict['response']['docs']) <= x:
                break

            result = search_dict['response']['docs'][x]

            #solr data does not explicitly stored type
            #so using unique fields to determine which model belongs to
            table = Game
            if 'country' in result:
                table = Company
            elif 'online_support' in result:
                table = Platform

            #add to results
            entity = session.query(table).get(result['id'])
            if entity is None:
                continue
            res['results'] += [[entity.name, entity.id, entity.deck, entity.description]]
            res['status'] = 0
            counted += 1

        #no hits, means no matches
        if counted == 0:
            res['message'] = 'No Matching Terms Found'

    except Exception as e:
        res['message'] = str(e)
    
    res['counted'] = counted

    return Response(to_json(res), mimetype='application/json', status=404 if res['status'] else 200)

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


@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get(
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
