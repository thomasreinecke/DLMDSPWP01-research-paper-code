import sqlite3
import os

# Path to the database
db_path = 'data/stock_data.db'
journal_path = 'data/stock_data.db-journal'

# Remove the existing database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Remove the journal file if it exists
if os.path.exists(journal_path):
    os.remove(journal_path)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the stocks table
cursor.execute('''
CREATE TABLE stocks (
    symbol TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    industry TEXT
)
''')

# Create the timeseries table
cursor.execute('''
CREATE TABLE timeseries (
    symbol TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
)
''')

# Create an index on the symbol column in the timeseries table to speed up joins
cursor.execute('''
CREATE INDEX idx_symbol_timeseries ON timeseries(symbol)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database schema with indexes has been successfully recreated.")
