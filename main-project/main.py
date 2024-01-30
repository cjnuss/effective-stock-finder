from elasticsearch import Elasticsearch
from flask import Flask, render_template

print("hello world!")

app = Flask(__name__)

def function_to_pass():
    return "Hello world"

def function_to_pass_2():
    return "Buy this stock because blah blah"

@app.route('/')
def index():
    flaskText1 = function_to_pass()
    flaskText2 = function_to_pass_2()
    
    # passing 2 strings to HTML
    return render_template('index.html', flaskText1 = flaskText1, flaskText2 = flaskText2) 

if __name__ == '__main__':
    app.run(debug=True)
    