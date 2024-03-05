from elasticsearch import Elasticsearch, helpers
import os
import re
import tsv_parser
import tsvGenerator

from es_functions import *

es = get_es()

top5stocks = get_top_five(es)

for stock in top5stocks:
  #the stock variable is a list of documents
  for document in stock:
    #a document is the list of information that has 4 strings in it
    print(document, end='\n\n')
  print('\n\n\n\n')
    
  