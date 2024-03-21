import yfinance as yf


index = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^NDX"]
names = ["S&P 500", "Dow 30", "Nasdaq", "Russell 2000", "Nasdaq 100"]
for ticker in index:
    ticker_data = yf.Ticker(ticker)
    index_data = ticker_data.history(period="1d", start="2023-01-01", end="2023-12-31")
    print(index_data)