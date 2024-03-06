from elasticsearch import Elasticsearch, helpers
import os
import re
import tsv_parser
import tsvGenerator

from es_functions import *

#keep this line commented out unless you want to wait 20 mins
#this line will...
#parse the tsv
#delete anything that is 3 days or older from the 'stockinfo' index
#add new documents to the 'stockinfo' index
#clear the 'bstring_ws' index completely
#refill the 'bstring_ws' index with P's and A's for each stock
#update_database()



es = get_es()
#this line gets the top 5 stocks and their documents
top5stocks = get_top_five(es)




#here is me printing out the results, you can do whatever you want with them
#this is just to show what the format of the variable top5stocks is like
for stock in top5stocks:
  #the stock variable is a list of documents
  for document in stock:
    #a document is the list of information that has 4 strings in it
    print(document, end='\n\n')
  print('\n\n\n\n')
    
  
