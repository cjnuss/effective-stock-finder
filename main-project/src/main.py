from elasticsearch import Elasticsearch
from flask import Flask, render_template
import random

class Stock:
    def __init__(self,name,short_name,price,percentage_change,price_change):
        self.name = name
        self.short_name = short_name
        self.price = price
        self.percentage_change = percentage_change
        self.price_change = price_change
    
    def create_stocks_test():
        apple = Stock("Apple, Inc.", "AAPL", "100", "11", "11")
        microsoft = Stock("Microsoft", "MSFT", "100", "11", "11")
        google = Stock("Google", "GOOG", "100", "11", "11")
        amazon = Stock("Amazon", "AMZN", "100", "11", "11")
        tesla = Stock("Tesla", "TLSA", "100", "11", "11")
        facebook = Stock("Facebook", "FB", "100", "11", "11")
        nvidia = Stock("NVIDIA", "NNVDA", "100", "11", "11")
        amd = Stock("AMD", "AMD", "100", "11", "11")
        netflix = Stock("Netflix", "NFLX", "100", "11", "11")
        intc = Stock("INTC", "INTC", "100", "11", "11")
        paypal = Stock("PayPal", "PYPL", "100", "11", "11")

        return [apple, microsoft, google, amazon, tesla, facebook, nvidia, amd, netflix, intc, paypal]

def GetDataFromGPT():
    stock_names = Stock.create_stocks_test()
    
    # Scramble the array
    random.shuffle(stock_names)
    
    # Select a random number of elements from 1 to 10
    num_elements = random.randint(1, min(len(stock_names), 10))
    
    # Take the first num_elements from the scrambled array
    selected_stock_names = stock_names[:num_elements]
    return selected_stock_names

app = Flask(__name__)



@app.route('/')
def index():

    
    return render_template('index.html', variables=GetDataFromGPT())

if __name__ == '__main__':
    app.run(debug=True)