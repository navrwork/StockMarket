import yfinance as yf

try:
    print(yf.download("NIFTYBEES.NS", period="1d").head()) #Try to download just one day of data
except Exception as e:
    print(f"Error: {e}")
