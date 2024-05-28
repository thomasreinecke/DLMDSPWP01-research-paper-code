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
    symbol TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    sector TEXT,
    industry TEXT
)
''')

# Create the timeseries table
cursor.execute('''
CREATE TABLE timeseries (
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    FOREIGN KEY (symbol) REFERENCES stocks (symbol),
    PRIMARY KEY (symbol, date)
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


# # Create the performance table
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS performance_data (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     symbol TEXT NOT NULL,
#     strategy_name TEXT NOT NULL,
#     strategy_end_balance REAL NOT NULL,
#     strategy_absolute_performance REAL NOT NULL,
#     strategy_total_percentage_performance REAL NOT NULL,
#     strategy_annual_avg_performance REAL NOT NULL,
#     benchmark_end_balance REAL NOT NULL,
#     benchmark_absolute_performance REAL NOT NULL,
#     benchmark_total_percentage_performance REAL NOT NULL,
#     benchmark_annual_avg_performance REAL NOT NULL,
#     outperformance_factor REAL NOT NULL,
#     is_strategy_more_profitable BOOLEAN NOT NULL,
#     FOREIGN KEY (symbol) REFERENCES stocks(symbol)
# );
# '''