import pandas as pd
import sqlite3
import os

# Paths to the files and database
constituents_path = "data/sp500_constituents.csv"
timeseries_dir = "data/timeseries"
db_path = "data/stock_data.db"

# Read the CSV file containing the S&P 500 constituents
df_constituents = pd.read_csv(constituents_path)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert data into the stocks table
for index, row in df_constituents.iterrows():
    cursor.execute('''
        INSERT INTO stocks (symbol, name, sector, industry) VALUES (?, ?, ?, ?)
    ''', (row['Symbol'], row['Security'], row['GICS Sector'], row['GICS Sub-Industry']))

# Iterate through each stock symbol in the DataFrame to load timeseries data
for index, row in df_constituents.iterrows():
    symbol = row['Symbol']
    # Path to the respective timeseries CSV file
    timeseries_path = os.path.join(timeseries_dir, f"{symbol}-eod.csv")
    
    # Check if the timeseries file exists
    if os.path.exists(timeseries_path):
        # Read the timeseries data
        df_timeseries = pd.read_csv(timeseries_path)
        
        # Insert data into the timeseries table
        for idx, ts_row in df_timeseries.iterrows():
            cursor.execute('''
                INSERT INTO timeseries (symbol, date, open, high, low, close, volume) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol, 
                ts_row['Date'], 
                ts_row['Open'], 
                ts_row['High'], 
                ts_row['Low'], 
                ts_row['Close'], 
                ts_row['Volume']))
    
    # Print the progress
    print(f"Loaded timeseries data for {index + 1}/{len(df_constituents)}: {symbol}")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Timeseries data has been successfully loaded into the database.")
