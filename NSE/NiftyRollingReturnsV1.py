import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_nifty_rolling_returns(indices, start_date, end_date, rolling_period=5):
    """
    Analyze 5-year rolling returns for multiple Nifty indices
    
    Parameters:
    -----------
    indices : list
        List of Nifty index ticker symbols
    start_date : str
        Start date for analysis (format: 'YYYY-MM-DD')
    end_date : str
        End date for analysis (format: 'YYYY-MM-DD')
    rolling_period : int
        Rolling period in years (default: 5)
    
    Returns:
    --------
    dict: Rolling returns data for each index
    """
    # Download data for each index
    rolling_returns = {}
    
    for index in indices:
        # Adjust ticker if needed
        ticker = index #if '.NS' in index else index + '.NS'
        
        # Download data
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            print(f"No data found for {ticker}")
            continue
        
        # Calculate annual rolling returns
        annual_returns = data['Close'].resample('YE').last().pct_change() * 100
        
        # Calculate 5-year rolling returns
        rolling_5y_returns = annual_returns.rolling(window=rolling_period).apply(
            lambda x: ((1 + x/100).prod() - 1) * 100
        )
        
        rolling_returns[index] = rolling_5y_returns
    
    # Visualization
    # plt.figure(figsize=(15, 6))
    
    # Plot rolling returns
    # for index, returns in rolling_returns.items():
    #     plt.plot(returns.index, returns.values, label=index)
    
    # plt.title(f'{rolling_period}-Year Rolling Returns of Nifty Indices')
    # plt.xlabel('Date')
    # plt.ylabel(f'{rolling_period}-Year Rolling Returns (%)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()
    
    return rolling_returns

# Example usage
if __name__ == "__main__":
    # List of Nifty indices to analyze
    indices_to_compare = [
        '^NSEI',  # Nifty 50
        'ICICIMOM30.NS',
        'MOMENTUM50.NS',
        'ALPHA.NS',
        'ALPL30IETF.NS',
        'MIDSMALL.NS',
        'SMALLCAP.NS'
       # '^NSEBANK',  # Nifty Bank
       # '^CNXIT',  # Nifty IT
    ]
    
    # Set date range for analysis (ensure it's longer than 5 years)
    start_date = '2015-01-25'
    end_date = '2025-01-25'
    rolling_period = 2

    # Perform rolling returns analysis
    rolling_returns = analyze_nifty_rolling_returns(
        indices_to_compare, 
        start_date, 
        end_date,
        rolling_period
    )
    
    # Optional: Save results to CSV
    for index, returns in rolling_returns.items():
        returns.to_csv(f'data/{index}_{rolling_period}y_rolling_returns.csv')

# Additional analysis function
def compare_rolling_returns(rolling_returns):
    """
    Compare and summarize rolling returns
    """
    summary = pd.DataFrame(columns=['Mean Return', 'Max Return', 'Min Return', 'Std Dev'])
    
    for index, returns in rolling_returns.items():
        summary.loc[index] = [
            returns.mean(),
            returns.max(),
            returns.min(),
            returns.std()
        ]
    
    print("\nRolling Returns Summary:")
    print(summary)
    return summary
