from elasticsearch import Elasticsearch, helpers
import os
import re

from es_functions import *

es = get_es()


res = es.search (index="newsgroup", body={"query": {"match": {"doc":{"query": "pain", "fuzziness": "AUTO"}}}}, size =10000)
print(len(res["hits"]["hits"]))
for doc in res["hits"]["hits"]:
  print(doc)


print("hello world!")