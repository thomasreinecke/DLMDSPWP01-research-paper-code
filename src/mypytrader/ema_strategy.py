# src/pytrader/ema_strategy.py
import vectorbt as vbt
import pandas as pd
from .strategy import Strategy

class EMA_Strategy(Strategy):
    def __init__(self, fast_window=12, slow_window=26):
        self.fast_window = fast_window
        self.slow_window = slow_window

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

        # Calculate the fast and slow EMA
        fast_ema = vbt.MA.run(data['close'], window=self.fast_window, short_name='fast')
        slow_ema = vbt.MA.run(data['close'], window=self.slow_window, short_name='slow')

        # Generate buy and sell signals
        entries = fast_ema.ma_crossed_above(slow_ema)
        exits = fast_ema.ma_crossed_below(slow_ema)

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
        return "EMA"
