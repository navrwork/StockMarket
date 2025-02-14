import yfinance as yf
import pandas as pd

def get_close_and_200dma(ticker, years):
    # Calculate the period in days
    period = f"{years * 365}d"
    
    # Download historical data for the given ticker
    data = yf.download(ticker, period=period)

    # Calculate the 200-day moving average (200 DMA)
    data['200DMA'] = data['Close'].rolling(window=200, min_periods=200).mean()

    #data = data.dropna(subset=['200DMA'])

    data.columns = ['Close', 'High', 'Low', 'Open', 'Volume', '200DMA']

    #data_200dma = data['Close'].rolling(window=200, min_periods=200).mean()
    #data_close = data['Close']

    #print(data)

    #df = pd.DataFrame(data)

    #df.iat[0, 5] = ticker

    #print(f"data_200dma={data_200dma}")
    #print(f"data_close={data_close}")

    comparison_results = []
    row_count = 0
    days_total = 0
    days_below200dma = 0
    days_above200dma = 0

    for index, row in data.iterrows():
        row_count += 1
        if row_count > 200:
            days_total += 1
            if row['Close'] > row['200DMA']:
                comparison_results.append('FALSE')
                days_above200dma += 1
            else:
                comparison_results.append('TRUE')
                days_below200dma += 1

            # if data_close < data_200dma:
            #     data['IsBelow200DMA'] = True
            # else:
            #     data['IsBelow200DMA'] = False
        else:
            comparison_results.append('NA')

    data['IsBelow200DMA'] = comparison_results


    # Drop rows with NaN values in the 200DMA column
    # data = data.dropna(subset=['200DMA'])

    # Write the output to a CSV file
    data.to_csv(f"data/{ticker}_200dma_data.csv")

    days_above200dma_pct = (days_above200dma/days_total)*100
    days_below200dma_pct = 100 - days_above200dma_pct

    ### Print Summary ###
    print(f"ticker: {ticker}")
    print(f"years: {years}")
    print(f"days_total: {days_total}")
    print(f"days_above200dma: {days_above200dma}, pct={days_above200dma_pct:.2f}")
    print(f"days_below200dma: {days_below200dma}, pct={days_below200dma_pct:.2f}")
    print(f"{ticker},{days_total},{days_below200dma},{days_below200dma_pct:.2f}")

    return data[['Close', '200DMA']]

# Example usage
ticker = "NIFTYBEES.NS"
years = 5
data = get_close_and_200dma(ticker, 5)
data = get_close_and_200dma(ticker, 3)
print(f"The 200 DMA values for {ticker} have been written to data/{ticker}_200dma_data.csv")
