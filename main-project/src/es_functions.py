from elasticsearch import Elasticsearch, helpers
import os
import re
import time
import tsv_parser
#Comment this out when generator is not being used
#import tsvGenerator
from datetime import datetime, timedelta




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
    print("dump done")

def create_new_index(es, indexname):
    es.indices.create(index=indexname, ignore=400)

#clears the bonsai/elasticsearch database of anything with the inputed index
def clear_es_index(es, indexname):
    query = {
        "query": {
            "match_all": {}
        }
    }
    res = es.delete_by_query(index=indexname, body=query)
    print("cleared index: {}".format(indexname))
    
    
def clear_old_data(es):
    three_days_ago = datetime.now() - timedelta(days=3)
    three_days_ago_str = three_days_ago.strftime("%Y-%m-%d")
    query = {
        "query": {
            "range": {
                "date": {
                    "lt": three_days_ago_str
                }
            }
        }
    }
    res = es.delete_by_query(index='stockinfo', body=query)
    print("cleared data from before: {}".format(three_days_ago_str))
    
    
    
    





#this is how you make the docs variable that you will feed into dump_documents
#l is a list of lists 
#the lists should contain strings for each section of the document
#the returned thing named docs is a list of dictionaries
def make_docs(l, indexname):
    docs = list()

    for thing in l:
        transaction_code = thing[0]
        footnote = thing[1]
        issuer_name = thing[2]
        issuer_trading_symbol = thing[3]
        price = thing[4]
        volume = thing[5]
        date = thing[6]
        #add more here and below
        
        doc = dict() 
        doc["_op_type"] = 'index'
        doc["_index"] = indexname
        doc["transaction code"] = transaction_code
        doc["footnote"] = footnote
        doc["issuer name"] = issuer_name
        doc["issuer trading symbol"] = issuer_trading_symbol
        doc["price"] = price
        doc["volume"] = volume
        doc["date"] = date
        
        #if doc not in docs:
        docs.append(doc)
        
    return docs













def make_bstrings_ws(es):
    #get all the documents
    res = es.search (index="stockinfo", body={"query": {"match_all": {}}},size=10000)
    
    docs = list()
    symbols = {}
    #used for price and stuff
    symbolsP = {}
    symbolsS = {}

    for doc in res["hits"]["hits"]:
        transaction_code = doc['_source']['transaction code']
        footnote = doc['_source']['footnote']
        issuer_name = doc['_source']['issuer name']
        issuer_trading_symbol = doc['_source']['issuer trading symbol']
        price = doc['_source']['price']
        volume = doc['_source']['volume']
        date = doc['_source']['date']
        #add more here and below
        
        #building str
        if issuer_trading_symbol not in symbols:
            symbols[issuer_trading_symbol] = transaction_code
        else:
            symbols[issuer_trading_symbol] += " " + transaction_code
        
        product = float(price)*float(volume)    
        #building P  
        if transaction_code == 'P':
            if issuer_trading_symbol not in symbolsP:
                symbolsP[issuer_trading_symbol] = product
            else:
                symbolsP[issuer_trading_symbol] += product
        #building S
        if transaction_code == 'S':
            if issuer_trading_symbol not in symbolsS:
                symbolsS[issuer_trading_symbol] = product
            else:
                symbolsS[issuer_trading_symbol] += product
        
    
    for key, value in symbols.items():
        doc = dict() 
        doc["_op_type"] = 'index'
        doc["_index"] = 'bstring_ws'
        doc["symbol"] = key
        doc["str"] = value
        if key in symbolsP and key in symbolsS:
            doc["PtoS_ratio"] = symbolsP[key]/symbolsS[key]
        elif key in symbolsP:
            doc["PtoS_ratio"] = 1000000
        elif key in symbolsS:
            doc["PtoS_ratio"] = -1
        
        if key in symbolsP:
            doc["Pamount"] = symbolsP[key]
        else:
            doc["Pamount"] = 0
        
        docs.append(doc)
        
    return docs





def get_top_ten(es):
    #this query will get the top 10 stocks based on boosting
    res = es.search (index="bstring_ws", body={"query": {
        "query_string": {
        "query": "(P)^3.5 (S)^4.5",
        "default_field": "str"
        }
    }}, size=10)


    top_ten = []
    #prints the top 10 along with the scores
    print(len(res["hits"]["hits"]))
    for doc in res["hits"]["hits"]:
        print(doc["_score"],end="   ")
        print(doc["_source"])
        top_ten.append(doc['_source']['symbol'])
    print()

    #info is a list with 10 lists, each of them represents a stock
    #each of these stock lists will be a list of things "articles" idk what they're called
    #each article will be a list of 4 things that you gave me 
    info = []
    for stock in top_ten:
        res = es.search (index="stockinfo", body={"query": {"match": {"issuer trading symbol": stock}}})
        documents = []
        for doc in res["hits"]["hits"]:
            li = []
            li.append(doc['_source']['transaction code'])
            li.append(doc['_source']['footnote'])
            li.append(doc['_source']['issuer name'])
            li.append(doc['_source']['issuer trading symbol'])
            li.append(doc['_source']['date'])
            #get rid of duplicates
            if li not in documents:
                documents.append(li)
        info.append(documents)
    
    return info




#parse the tsv
#delete anything that is 3 days or older from the 'stockinfo' index
#clear the 'bstring_ws' index completely
#add new documents to the 'stockinfo' index
#refill the 'bstring_ws' index with P's and A's for each stock
def update_database():
    lol = tsv_parser.tsv_to_data()
    es = get_es()
    
    clear_old_data(es)
    clear_es_index(es, "bstring_ws")
    
    docs = make_docs(lol, "stockinfo")
    dump_documents(es, docs)
    
    es = get_es()
    
    docs3 = make_bstrings_ws(es)
    dump_documents(es, docs3)
    













#LINES TO USE LATER IN MAIN OR SOME OTHER THING

#lol = tsv_parser.tsv_to_data()


#to clear the current stockinfo index
#clear_es_index(es, "stockinfo")
#clear_es_index(es, "bstring_ws")


#when making a new index
#create_new_index(es, "stockinfo")

#docs = make_docs(lol, "stockinfo")
#docs2 = make_bstrings(lol)
#docs3 = make_bstrings_ws(lol)

#dump_documents(es, docs)

#search by match
#res = es.search (index="stockinfo", body={"query": {"match": {"footnote": "employees"}}})

#search by fuzziness
#res = es.search (index="bstring_ws", body={"query": {"match": {"str":{"query": "A", "fuzziness": "AUTO"}}}}, size =10000)

# res = es.search (index="bstring_ws", body={"query": {
#     "query_string": {
#       "query": "(P)^2 (A)",
#       "default_field": "str"
#     }
#   }})

# print(len(res["hits"]["hits"]))
# for doc in res["hits"]["hits"]:
#   print(doc)
  












# res = es.search (index="bstring_ws", body={
#   "query": {
#     "function_score": {
#       "query": {
#         "match_all": {}
#       },
#       "functions": [
#         {
#           "filter": { "match": { "str": "A" } },
#           "weight": 2.2
#         },
#         {
#           "filter": { "match": { "str": "P" } },
#           "weight": 2.5
#         }
#       ]
#     }
#   }
# }, size=1150)