import pandas as pd  # pandas for data manipulation
import yfinance as yf  # yfinance to fetch stock data
import os  # os to handle directory creation

# Read the CSV file containing the S&P 500 constituents
df = pd.read_csv("data/sp500_constituents.csv")

# Directory to save the timeseries data
os.makedirs("data/timeseries", exist_ok=True)  # Create the directory if it doesn't exist

# Iterate through each stock symbol in the DataFrame
for index, row in df.iterrows():
    symbol = row['Symbol']
    company_name = row['Security']
    
    # Fetch the end-of-day timeseries data using yfinance with progress output suppressed
    stock_data = yf.download(symbol, progress=False)
    
    # Save the timeseries data to a CSV file
    stock_data.to_csv(f"data/timeseries/{symbol}-eod.csv")
    
    # Print the progress
    print(f"Processed {index + 1}/{len(df)}: {symbol} - {company_name}")

print("Timeseries data has been successfully saved.")
