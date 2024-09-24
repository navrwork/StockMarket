import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

from datetime import date
from dateutil.relativedelta import relativedelta

def main():
    avg_num_of_trading_days_in_a_year = 252
    num_of_years = 5
    total_trading_days = num_of_years * avg_num_of_trading_days_in_a_year

    # Get today's date
    today = date.today()

    # Subtract X years from today's date
    x_years_ago = today - relativedelta(years=num_of_years)

    ## Ticket list
    # ^NSEI NIFTYBEES ITBEES.NS PHARMABEES.NS FMCGIETF.NS

    ## Set Index value here
    ticker = "NIFTYBEES.NS"

    # Fetch historical data for Nifty 50
    nifty_data = yf.download(ticker, start=x_years_ago, end=today)

    # Calculate the 20-day moving average
    nifty_data['20DMA'] = nifty_data['Close'].rolling(window=20).mean()
    nifty_data['50DMA'] = nifty_data['Close'].rolling(window=50).mean()

    start_date = nifty_data.index.min().date()
    ticker_age = days_between(start_date, today)
    ticker_age_in_months = round(ticker_age/30)
    if (ticker_age < total_trading_days):
        total_trading_days = ticker_age


    # Identify days when the closing price is below the 20/50 DMA
    below_20dma = nifty_data[nifty_data['Close'] < nifty_data['20DMA']]
    below_50dma = nifty_data[nifty_data['Close'] < nifty_data['50DMA']]

    close_in_red = nifty_data[nifty_data['Close'] < nifty_data['Open']]

    # Count the number of days
    num_days_below_20dma = below_20dma.shape[0]
    num_days_below_50dma = below_50dma.shape[0]
    num_days_close_in_red = close_in_red.shape[0]

    # percentage
    pct_below_20dma = (num_days_below_20dma/total_trading_days)*100
    pct_below_50dma = (num_days_below_50dma/total_trading_days)*100
    pct_close_in_red = (num_days_close_in_red/total_trading_days)*100

    # Print stats
    print("#############################################################")
    print(f"Ticker: {ticker}")
    print(f"Ticker first trade on: {start_date}. Ticker age: {total_trading_days} days / {ticker_age_in_months} months")
    print("--------------------------------------------------------------")
    print(f"Number of days {ticker} traded below 20 DMA: {num_days_below_20dma}")
    print(f"Percentage of trade below 20 DMA: {pct_below_20dma:.2f}%")
    print("--------------------------------------------------------------")
    print(f"Number of days {ticker} traded below 50 DMA: {num_days_below_50dma}")
    print(f"Percentage of trade below 50 DMA: {pct_below_50dma:.2f}%")
    print("--------------------------------------------------------------")
    print(f"Number of days {ticker} closed in Red: {num_days_close_in_red}")
    print(f"Percentage of trade closed in Red: {pct_close_in_red:.2f}%")
    print("#############################################################")

    # Plot the closing prices and 20 DMA
    plt.figure(figsize=(14,7))
    plt.plot(nifty_data['Close'], label='Close')
    plt.plot(nifty_data['20DMA'], label='20 DMA', color='orange')
    plt.title(f"Ticker: {ticker}. Closing Prices and 20-Day Moving Average")
    plt.legend()
    plt.show()

def days_between(d1, d2):
    #d1 = date.datetime.strptime(d1, "%Y-%m-%d")
    #d2 = date.datetime.strptime(d2, "%Y-%m-%d")
    #d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


main()