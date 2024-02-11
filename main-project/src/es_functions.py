from elasticsearch import Elasticsearch, helpers
import os
import re





#this will get you an istance of es (bonsai version)
def get_es():
    #bonsai = os.environ['BONSAI_URL']
    bonsai = "https://838alqklx3:odrdceak9j@stonks-up-search-7220409407.us-east-1.bonsaisearch.net:443"
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    # optional port
    match = re.search('(:\d+)', host)
    if match:
        p = match.group(0)
        host = host.replace(p, '')
        port = int(p.split(':')[1])
    else:
        port=443

    # Connect to cluster over SSL using auth for best security:
    es_header = [{
        'host': host,
        'port': port,
        'use_ssl': True,
        'http_auth': (auth[0],auth[1])
    }]

    # Instantiate the new Elasticsearch connection:
    es = Elasticsearch(es_header)
    return es










#this will dump whatever is in the docs variable into the database/bonsai/es
def dump_documents(es, docs):
    # print(docs)
    helpers.bulk(es, docs )
    #print("dump done")












#clears the bonsai/elasticsearch database of anything with the inputed index
def clear_es_index(es, indexname):
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = es.delete_by_query(index=indexname, body=query)
    
    
    
    
    





#this is how you make the docs variable that you will feed into dump_documents
#l is a list of lists 
#the lists should contain strings for each section of the document
#the returned thing named docs is a list of dictionaries
def make_docs(l, indexname):
    docs = list()

    for thing in l:
        title = thing[0]
        content = thing[1]
        link = thing[2]
        #add more here and below
        
        doc = dict() 
        doc["_op_type"] = 'index'
        doc["_index"] = indexname
        doc["title"] = title
        doc["content"] = content
        doc["link"] = link
        docs.append(doc)
        
    return docs




