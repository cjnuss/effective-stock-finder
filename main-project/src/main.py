from elasticsearch import Elasticsearch, helpers
import os
import re
from flask import Flask, render_template, redirect, url_for, request
import random
#Comment this out if its not being used
#import tsvGenerator

from es_functions import *

class Stock:
    def __init__(self,name,short_name,price,percentage_change,price_change,reason):
        self.name = name
        self.short_name = short_name
        self.price = price
        self.percentage_change = percentage_change
        self.price_change = price_change
        self.reason = reason

    def random_recommendations():
        apple = Stock("Apple, Inc.", "AAPL", "100", "11", "11", "dfadsfdasfdas.")
        microsoft = Stock("Microsoft", "MSFT", "100", "-1", "-1", "ddsafdasfdasfdsaf.")
        google = Stock("Google", "GOOG", "100", "11", "11", "ddsafdasfdsafsda.")
        amazon = Stock("Amazon", "AMZN", "100", "11", "11", "dfdsafdsa.")
        tesla = Stock("Tesla", "TLSA", "100", "-11", "-11", "dfadsfdsaf.")
        facebook = Stock("Facebook", "FB", "100", "11", "11", "sadfasdfdsafd.")
        nvidia = Stock("NVIDIA", "NNVDA", "100", "-11", "-11", "sdasadfdsafdasd.")
        amd = Stock("AMD", "AMD", "100", "11", "11", "dafadsfdasfsda.")
        netflix = Stock("Netflix", "NFLX", "100", "0", "0", "dfadsfdsafdsa.")
        intc = Stock("INTC", "INTC", "100", "11", "11", "dfdsafdasfas.")
        paypal = Stock("PayPal", "PYPL", "100", "0", "0", "ddfasfadsfdas.")

        if switch.getContent() == 1:
            return [nvidia]

        stock_names = [apple, microsoft, google, amazon, tesla, facebook, nvidia, amd, netflix, intc, paypal]
        
        # Scramble the array
        random.shuffle(stock_names)
        
        # Select a random number of elements from 1 to 10
        # num_elements = random.randint(1, min(len(stock_names), 10))
        
        # Take the first num_elements from the scrambled array
        selected_stock_names = stock_names[0:8]
        return selected_stock_names
    

class Switch:
    def __init__(self):
        self.content = ""
    
    def change(self, content):
        self.content = content
    
    def getContent(self):
        return self.content

app = Flask(__name__)
switch = Switch()

@app.route('/')
def index():
    return render_template('index.html', variables=Stock.random_recommendations(), switch=switch.getContent())

@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    if request.form.get('refresh') == 'true':
        switch.change(1)

    return redirect(url_for('index'))

@app.route('/refresh', methods=['POST'])
def refresh():
    switch.change("")
    return 'Signal received'

if __name__ == '__main__':
    app.run(debug=True)
    #---
#keep this line commented out unless you want to wait 20 mins
#this line will...
#parse the tsv
#delete anything that is 3 days or older from the 'stockinfo' index
#add new documents to the 'stockinfo' index
#clear the 'bstring_ws' index completely
#refill the 'bstring_ws' index with P's and A's for each stock
#---

#update_database()



es = get_es()
#this line gets the top 5 stocks and their documents
top5stocks = get_top_five(es)



#here is me printing out the results, you can do whatever you want with them
#this is just to show what the format of the variable top5stocks is like
#for stock in top5stocks:
  #the stock variable is a list of documents
 # for document in stock:
    #a document is the list of information that has 4 strings in it
  #  print(document, end='\n\n')
  #print('\n\n\n\n')