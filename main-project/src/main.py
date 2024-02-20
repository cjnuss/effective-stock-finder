from elasticsearch import Elasticsearch, helpers
import os
import re
import tsv_parser

from es_functions import *

es = get_es()

#lol = tsv_parser.tsv_to_data()

#to clear the current stockinfo index
#clear_es_index(es, "stockinfo")

#when making a new index
#create_new_index(es, "stockinfo")

#docs = make_docs(lol, "stockinfo")

#dump_documents(es, docs)

#search by match
#res = es.search (index="stockinfo", body={"query": {"match": {"footnote": "install"}}})

#search by fuzziness
res = es.search (index="stockinfo", body={"query": {"match": {"footnote":{"query": "employees", "fuzziness": "AUTO"}}}}, size =10000)

print(len(res["hits"]["hits"]))
for doc in res["hits"]["hits"]:
  print(doc)
