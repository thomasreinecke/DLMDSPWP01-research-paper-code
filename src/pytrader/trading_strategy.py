from abc import ABC, abstractmethod
import pandas as pd

class TradingStrategy(ABC):
    @abstractmethod
    def calculate_trades(self, symbol: str, data: pd.DataFrame, start_amount: float):
        pass

    def execute_strategy(self, symbol: str, data: pd.DataFrame, start_amount: float):
        trades, balance_timeseries, summary = self.calculate_trades(symbol, data, start_amount)
        return {
            'trades': trades,
            'balance_timeseries': balance_timeseries,
            'summary': summary
        }
