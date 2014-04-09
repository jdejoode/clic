from flask import Flask
import json

app = Flask(__name__,static_url_path='')

import re

## Use beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


from dickens.keywords import Keywords
from dickens.clusters import Clusters
from dickens.concordance_new import Concordancer_New

from flask import request
from flask import render_template


cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@app.route('/keywords/',methods=['GET'])
def keywords():
    args = request.args
    print args

    # put keywords into json
    keyword_result = fetchKeywords(args)
    #print keyword_result
    keywords = json.dumps(keyword_result)

    return render_template('keywords.html', keywords=keywords)

## ajax route: for splitting screen
@app.route('/ajax-keywords',methods=['GET'])
def ajax_keyords():
    args = request.args
    return json.dumps(fetchKeywords(args))


@app.route('/clusters/', methods=['GET'])
def clusters():
    args = request.args
    
    clusters_result = fetchClusters(args)
    clusters = json.dumps(clusters_result)

    return render_template('clusters.html', clusters=clusters)

@app.route('/concordances/',methods=['GET'])
def concordances():
    args = request.args  

    concordances_result = fetchConcordance(args)
    concordances = json.dumps(concordances_result)

    return render_template('concordances.html', concordances=concordances)


#@cache.cache('keyword', expire=3600) ## expires after 3600 secs
def fetchKeywords(args):

    keyworder = Keywords()
    args = processArgs(args, 'keywords')
    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3])
    return {'keywords':keywords}

#@cache.cache('cluster', expire=3600)
def fetchClusters(args):

    cluster = Clusters()
    
    args = processArgs(args, 'clusters')
 
    clusterlist = cluster.list_clusters(args[0], args[1])

    return {'clusters' : clusterlist}

#@cache.cache('concordances', expire=3600)
def fetchConcordance(args):

    concordancer = Concordancer_New()
    args = processArgs(args, 'concordances')
    print args
    concordances = concordancer.create_concordance(args[0], args[1], args[2], args[3], args[4])

    return {'concordances' : concordances}

def processArgs(args, method):
   
    methodArgs = []
    testMod = str(args["testIdxMod"])    

    if not method == 'concordances':
        Group = str(args['testIdxGroup']) ## testGroup not used in concordances
        testIdxName = "{0}-{1}".format(testMod, Group)
        methodArgs.insert(0, testIdxName)
        book_collection = args.getlist('testCollection') ## args is a multiDictionary: use .getlist() to access individual books
        methodArgs.insert(1, book_collection)

    if method == 'keywords':

        refMod = str(args['refIdxMod'])
        refbook_collection = args.getlist('refCollection') 

        refIdxName = "{0}-{1}".format(refMod, Group)

        ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
        ## THERE WILL BE DEFAULT SELECT IN INTERFACE
#         if not re.match('\dgram-idx', Group):
#             if not args['testIdxMod'] == '':
#                 testIdxName = testMod + '-idx'
#                 refIdxName = refMod + '-idx'
# 
#         else:
#             testIdxName = 'sentence-idx'
#             refIdxName = 'sentence-idx'

        methodArgs.insert(2, refIdxName)
        methodArgs.insert(3, refbook_collection)

    elif method == 'concordances':

        testIdxName = testMod + '-idx'
        wordWindow = str(args['wordWindow'])
        book_collection = args.getlist('testCollection')
        select_words = str(args['selectWords'])
        print select_words

        methodArgs.insert(0, str(args['terms']))
        methodArgs.insert(1, testIdxName)
        methodArgs.insert(2, wordWindow)
        methodArgs.insert(3, book_collection)    
        methodArgs.insert(4, select_words)    


    return methodArgs
