import yfinance as yf

try:
    response = yf.Ticker("ticker")
    print(response)
except Exception as e:
    print(f"An error occurred: {str(e)}")