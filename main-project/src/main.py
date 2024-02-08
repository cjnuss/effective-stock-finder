from elasticsearch import Elasticsearch
from flask import Flask, render_template
import random


def GetDataFromGPT():
    stock_names = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "AMD", "NFLX", "INTC", "PYPL", "ADBE"]
    
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