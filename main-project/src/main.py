from elasticsearch import Elasticsearch, helpers
import os
import re
from flask import Flask, render_template, redirect, url_for, request
import chat_analyzer
from es_functions import *
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

es = get_es()
#This line gets the top 10 stocks and their documents
top5stocks = get_top_ten(es)
#This gets the tickers, descriptions and company_names of top stocks
tickers, descriptions, company_names = chat_analyzer.getInformation(top5stocks)

#Custom round function to take care of stocks with very low prices
def custom_round(number):
    num_str = str(number)
    index = num_str.find('.')
    first_digit = 1
    second_digit = 1
    #Gets the first and second digits after the decimal or sets them to 1 if they don't exist (we only care about them if they are both 0)
    if index != -1:
        first_digit = int(num_str[index + 1])
        if index + 2 < len(num_str):
            second_digit = int(num_str[index + 2])

    #Rounds the number to first significant digit if number is less than 1 and first 2 digits after decimal point are 0
    if number < 1 and first_digit == 0 and second_digit == 0:
        for i in range(index + 1, len(num_str)):
            if num_str[i] != '0':
                rounded = int(num_str[i])
                if i + 1 < len(num_str) and int(num_str[i + 1]) >= 5:
                    rounded += 1
                result = float(num_str[:i] + str(rounded))
                break

    #Rounds larger numbers to 2 decimal places
    else:
        result = round(number, 2)
    return result

class Stock:
    #Initializes stock object
    def __init__(self,name,short_name,price,percentage_change,price_change,reason, high, low):
        self.name = name
        self.short_name = short_name
        self.price = price
        self.percentage_change = percentage_change
        self.price_change = price_change
        self.reason = reason
        self.high = high
        self.low = low

    def indexes():

        #Parallel lists containing prices, percentage change and price change
        prices = [] 
        percentage = [] 
        change = []
        high = []
        low = []

        #Lists containing index tickers and index names
        indexes = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^NDX"]
        names = ["S&P 500", "Dow 30", "Nasdaq", "Russell 2000", "Nasdaq 100"]

        #Get last trading day
        last_day = datetime.today().date()

        #Set the last trading day to Friday if its Saturday or Sunday
        if last_day.weekday() == 5:  
            last_day = last_day - timedelta(days=1)
        elif last_day.weekday() == 6:  
            last_day = last_day - timedelta(days=2)

        #Loops through the indexes and gets their closing data from last day
        for ticker in indexes:
            try:
                #Gets current index price
                response = yf.Ticker(ticker)
                price = custom_round(response.history(period="1d")["Close"].iloc[-1])
                prices.append(price)

                #Gets historical data from last trading day
                data = response.history(start=last_day, end=last_day+timedelta(days=1))
                open = data["Open"].iloc[0]
                close = data["Close"].iloc[0]
                latest_high = data["High"].iloc[0]
                latest_low = data["Low"].iloc[0]
                high.append(custom_round(latest_high))
                low.append(custom_round(latest_low))

                #Gets the price change from last trading day
                price_change = custom_round(close-open)
                change.append(price_change)

                #Gets the percentage price change from last trading day
                percentage_change = custom_round(((close-open)/open)*100)
                percentage.append(percentage_change)

            #Appends empty string if data is unavailable 
            except Exception as e:
                print(f"An error occurred: {e}")
                prices.append("")
                percentage.append("")
                change.append("")

        #Creates the stock objects for the indexes 
        index1 = Stock(names[0], indexes[0], prices[0], percentage[0], change[0], descriptions[0], high[0], low[0])
        index2 = Stock(names[1], indexes[1], prices[1], percentage[1], change[1], descriptions[1], high[1], low[1])
        index3 = Stock(names[2], indexes[2], prices[2], percentage[2], change[2], descriptions[2], high[2], low[2])
        index4 = Stock(names[3], indexes[3], prices[3], percentage[3], change[3], descriptions[3], high[3], low[3])
        index5 = Stock(names[4], indexes[4], prices[4], percentage[4], change[4], descriptions[4], high[4], low[4])

        stock_names = [index1, index2, index3, index4, index5]

        return stock_names
    
    #Sets up recommendations to display
    def recommendations(case): 
        
        #Parallel lists containing prices, percentage change and price change
        prices = [] 
        percentage = [] 
        change = []
        high = []
        low = []

        #Get last trading day
        last_day = datetime.today().date()

        #Set the last trading day to Friday if its Saturday or Sunday
        if last_day.weekday() == 5:  
            last_day = last_day - timedelta(days=1)
        elif last_day.weekday() == 6:  
            last_day = last_day - timedelta(days=2)

        #Loops through the stocks and gets their closing data from last day
        for ticker in tickers:
            try:
                #Gets current stock price
                response = yf.Ticker(ticker)
                price = custom_round(response.history(period="1d")["Close"].iloc[-1])
                prices.append(price)

                #Gets historical data from last trading day
                data = response.history(start=last_day, end=last_day+timedelta(days=1))
                open = data["Open"].iloc[0]
                close = data["Close"].iloc[0]
                latest_high = data["High"].iloc[0]
                latest_low = data["Low"].iloc[0]
                high.append(custom_round(latest_high))
                low.append(custom_round(latest_low))

                #Gets the price change from last trading day
                price_change = custom_round(close-open)
                change.append(price_change)

                #Gets the percentage price change from last trading day
                percentage_change = custom_round(((close-open)/open)*100)
                percentage.append(percentage_change)

            #Appends empty string if data is unavailable 
            except Exception as e:
                print(f"An error occurred: {e}")
                prices.append("")
                percentage.append("")
                change.append("")
                high.append("")
                low.append("")

        #Creates the stock objects for the best stocks
        stock1 = Stock(company_names[0], tickers[0], prices[0], percentage[0], change[0], descriptions[0], high[0], low[0])
        stock2 = Stock(company_names[1], tickers[1], prices[1], percentage[1], change[1], descriptions[1], high[1], low[1])
        stock3 = Stock(company_names[2], tickers[2], prices[2], percentage[2], change[2], descriptions[2], high[2], low[2])
        stock4 = Stock(company_names[3], tickers[3], prices[3], percentage[3], change[3], descriptions[3], high[3], low[3])
        stock5 = Stock(company_names[4], tickers[4], prices[4], percentage[4], change[4], descriptions[4], high[4], low[4])
        stock6 = Stock(company_names[5], tickers[5], prices[5], percentage[5], change[5], descriptions[5], high[5], low[5])
        stock7 = Stock(company_names[6], tickers[6], prices[6], percentage[6], change[6], descriptions[6], high[6], low[6])
        stock8 = Stock(company_names[7], tickers[7], prices[7], percentage[7], change[7], descriptions[7], high[7], low[7])
        stock9 = Stock(company_names[8], tickers[8], prices[8], percentage[8], change[8], descriptions[8], high[8], low[8])
        stock10 = Stock(company_names[9], tickers[9], prices[9], percentage[9], change[9], descriptions[9], high[9], low[9])
        #Picks the best stock 
        if case == 1:
            return [stock1]

        stock_names = [stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8, stock9, stock10]

        return stock_names

app = Flask(__name__)

#Renders home page
@app.route('/')
def index():
    return render_template('index.html', variables=Stock.recommendations(0), indexes=Stock.indexes())

#Renders page to display the 1 stock
@app.route('/best_stock')
def stock_recommendations():
    
    #Gets the date range for the data
    end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')
    #Gets lists of dates and closing prices for last 7 days including today
    hist_data = yf.download(tickers[0], start=start, end=end)
    closing_prices = hist_data['Close']
    dates = closing_prices.index.strftime('%Y-%m-%d').tolist()
    values = closing_prices.tolist()
    #Loops through all values to round them to 2 decimal places
    for i in range(len(values)):
        values[i] = custom_round(values[i])
    #Creates a dictionary for the data
    data = {
        'Date': dates,
        'Value': values
    }

    #Gets data into a format that can be displayed as a graph 
    df = pd.DataFrame(data)
    plot_data_json = df.to_json(orient='records')    
    #Sets the color of the graph line based on the stock trend over the week 
    if (data['Value'][-1]-data['Value'][0]) > 0:
       color = 'green'
    elif (data['Value'][-1]-data['Value'][0]) < 0:
       color = 'red'
    else:
       color = 'blue'
    return render_template('best_stock.html', variables=Stock.recommendations(1), plot_data=plot_data_json, color=color)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)             