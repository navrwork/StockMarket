import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from datetime import date
from dateutil.relativedelta import relativedelta

avg_num_of_trading_days_in_a_year = 252
num_of_years = 5
total_trading_days = num_of_years * avg_num_of_trading_days_in_a_year

print(f"Generating report for past {num_of_years} years ...")

# Get today's date
today = date.today()
#print("Today's date:", today)

# Subtract X years from today's date
x_years_ago = today - relativedelta(years=num_of_years)
#print(f"Date {5} years ago: ", num_of_years)

## Ticket list
# ^NSEI
# ITBEES.NS

## Set Index value here
index = "ALPHA.NS"

# Fetch historical data for Nifty 50
nifty_data = yf.download(index, start=x_years_ago, end=today)

# Calculate the 20-day moving average
nifty_data['20DMA'] = nifty_data['Close'].rolling(window=20).mean()
nifty_data['50DMA'] = nifty_data['Close'].rolling(window=50).mean()

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
print("#############################################################")
print(f"Number of years being considered: {num_of_years}")
print(f"Index being analyzed: {index}")
print(f"Today's date: {today}, Date {5} years ago: {x_years_ago}")
print(f"Total number of trading days (approx.): {total_trading_days}")
print(f"Number of days {index} traded below 20 DMA: {num_days_below_20dma}")
print(f"Percentage of trade below 20 DMA: {pct_below_20dma:.2f}%")
print("#############################################################")
print(f"Number of days {index} traded below 50 DMA: {num_days_below_50dma}")
print(f"Percentage of trade below 50 DMA: {pct_below_50dma:.2f}%")
print("#############################################################")
print(f"Number of days {index} closed in Red: {num_days_close_in_red}")
print(f"Percentage of trade closed in Red: {pct_close_in_red:.2f}%")
print("#############################################################")
print("#############################################################")

# Plot the closing prices and 20 DMA
plt.figure(figsize=(14,7))
plt.plot(nifty_data['Close'], label='Nifty 50 Close')
plt.plot(nifty_data['20DMA'], label='20 DMA', color='orange')
plt.title('Nifty 50 Closing Prices and 20-Day Moving Average')
plt.legend()
plt.show()
