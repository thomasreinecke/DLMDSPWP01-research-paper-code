# src/pytrader/strategy.py

from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    @abstractmethod
    def calculate(self, symbol: str, data: pd.DataFrame, start_amount: float, start_date: str, end_date: str):
        pass

    @abstractmethod
    def name(self) -> str:
        """Return the name of the strategy."""
        pass

    def run(self, symbol: str, data: pd.DataFrame, start_amount: float, start_date: str, end_date: str):
        pf = self.calculate(symbol, data, start_amount, start_date, end_date)
        from .strategy_helper import extract_results
        return extract_results(pf, data, symbol, start_amount, self.name())
