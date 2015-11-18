import pysolr
import json

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://104.130.23.111:8983/solr/4playdb', timeout=10)

def migrate():
    
    print ("Adding games.nohtml.json")

    with open('scripts/giantbomb/json/games.nohtml.json') as f:
        for i in json.load(f):
            solr.add([i])

    print ("Adding companies.nohtml.json")

    with open('scripts/giantbomb/json/companies.nohtml.json') as f:
        for i in json.load(f):
            solr.add([i])

    print ("Adding platforms.nohtml.json")

    with open('scripts/giantbomb/json/platforms.nohtml.json') as f:
        for i in json.load(f):
            solr.add([i])

    print ("Some sample queries")

def query():

    results = solr.search('mario', **{
        'hl': 'true',
        'hl.fl': 'name',
        'hl.fragsize': 0,
        'hl.simple.pre': '<span class="highlight">',
        'hl.simple.post': '</span>'
    })

    print(results.highlighting)
    print(results.grouped)

    # Just loop over it to access the results.
    for result in results:
        print("Found '{0}'.".format(result['name']))

query()