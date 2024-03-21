import yfinance as yf

# Input the start and end dates and the stock ticker symbol
start_date = "2020-01-01"
end_date = "2024-03-11"
symbol = "AAPL"

# Download the stock price data from Yahoo Finance API
data = yf.download(symbol, start=start_date, end=end_date)

# Calculate the short-term and long-term Simple Moving Averages (SMAs)
sma_short = data['Close'].rolling(window=50).mean()
sma_long = data['Close'].rolling(window=200).mean()

# Determine the Buy or Sell signals based on the SMA crossovers
signals = [None]*len(sma_short)
for i in range(1, len(sma_short)):
    if sma_short[i] > sma_long[i] and sma_short[i-1] <= sma_long[i-1]:
        signals[i] = 'Buy'
        print(f"Buy signal detected on {data.index[i].date()}")
    elif sma_short[i] < sma_long[i] and sma_short[i-1] >= sma_long[i-1]:
        signals[i] = 'Sell'
        print(f"Sell signal detected on {data.index[i].date()}")




