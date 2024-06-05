# src/pytrader/rsi_strategy.py
import vectorbt as vbt
import pandas as pd
from .strategy import Strategy

class RSI_Strategy(Strategy):
    def __init__(self, lower_border=30, upper_border=70):
        self.lower_border = lower_border
        self.upper_border = upper_border

    def calculate(self, symbol: str, data: pd.DataFrame, start_amount: float, start_date: str, end_date: str):
        # Ensure the DataFrame is not empty
        if data.empty:
            print(f"No data found for symbol: {symbol}")
            return None

        # Ensure the 'close' column is numeric
        if not pd.api.types.is_numeric_dtype(data['close']):
            print(f"Non-numeric data found for symbol: {symbol}")
            return None

        # Manually set the frequency of the data to business days (most common for stock data)
        data = data.asfreq('B')

        # Calculate the RSI
        rsi = vbt.RSI.run(data['close'])

        # Generate buy and sell signals based on the lower and upper borders
        entries = rsi.rsi < self.lower_border
        exits = rsi.rsi > self.upper_border

        # Run the portfolio with a starting balance
        pf = vbt.Portfolio.from_signals(
            data['close'], 
            entries, 
            exits, 
            init_cash=start_amount, 
            freq='1D'  # Set the frequency to 1 day
        )
        return pf

    def name(self) -> str:
        return "RSI"
