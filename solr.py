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
                result[key] = '...'.join(highlighted[key])
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

    print ("Done!")

def query():

    results = solr.search('puzzle game', **{
        'hl': 'true',
        'hl.fl': '*',
        'hl.fragsize': 30,
        'hl.snippets': '5',
        'hl.mergeContiguous': 'true',
        'hl.simple.pre': '<span class="highlight">',
        'hl.simple.post': '</span>',
        'hl.highlightMultiTerm': 'true'
    })

    results = normalize_results(results)

    for result in results:
        for a in result:
            print("\033[1m\033[91m{0}\033[0m: {1}".format(a, result[a]))
        print()