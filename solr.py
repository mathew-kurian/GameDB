import pysolr
import json

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://104.130.23.111:8983/solr/4playdb', timeout=10)

def normalize_results(results):
    # Just loop over it to access the results.
    for result in results:
        if result['id'] in results.highlighting:
            highlighted = results.highlighting[result['id']]
            for key in highlighted:
                result[key] = highlighted[key]
        for key in result:
            if type(result[key]) == list:
                result[key] = result[key][0]

    return results

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
        'hl.fl': 'name deck description',
        'hl.fragsize': 0,
        'hl.simple.pre': '<span class="highlight">',
        'hl.simple.post': '</span>'
    })

    results = normalize_results(results)

    for result in results:
        for a in result:
            print("\033[1m\033[91m{0}\033[0m: {1}".format(a, result[a]))
        print()