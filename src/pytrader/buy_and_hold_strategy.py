import pandas as pd
from .trading_strategy import TradingStrategy

class BuyAndHoldStrategy(TradingStrategy):
    def calculate_trades(self, symbol: str, data: pd.DataFrame, start_amount: float):
        cash = start_amount
        trades = []
        balance_history = []

        def balance(cash, current_price, quantity):
            return cash + (quantity * current_price)

        current_balance = start_amount
        years = data['date'].dt.year.unique()

        for year in years:
            year_data = data[data['date'].dt.year == year]
            if year_data.empty:
                continue

            # Buy at the first day of the year
            entry_date = year_data.iloc[0]['date']
            entry_price = year_data.iloc[0]['close']
            quantity = int(cash / entry_price)
            entry_amount = entry_price * quantity
            cash -= entry_amount
            trades.append({
                'index': len(trades),
                'symbol': symbol,
                'entry_amount': entry_amount,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'quantity': quantity,
                'exit_date': None,
                'exit_price': None,
                'pl': None,
                'exit_amount': None
            })

            # Update balance history throughout the year
            for date, row in year_data.iterrows():
                current_balance = balance(cash, row['close'], quantity)
                balance_history.append({'date': row['date'], 'balance': current_balance})

            # Sell at the last day of the year
            exit_date = year_data.iloc[-1]['date']
            exit_price = year_data.iloc[-1]['close']
            exit_amount = exit_price * quantity
            profit_loss = exit_amount - entry_amount
            cash += exit_amount
            trades[-1]['exit_date'] = exit_date
            trades[-1]['exit_price'] = exit_price
            trades[-1]['pl'] = profit_loss
            trades[-1]['exit_amount'] = exit_amount

        # Summary of the performance
        total_pl = sum(trade['pl'] for trade in trades if trade['pl'] is not None)
        total_trades = len(trades)
        profit_trades = sum(1 for trade in trades if trade['pl'] is not None and trade['pl'] > 0)
        loss_trades = total_trades - profit_trades

        summary = {
            'total_pl': total_pl,
            'total_trades': total_trades,
            'profit_trades': profit_trades,
            'loss_trades': loss_trades
        }

        trades_df = pd.DataFrame(trades).round(2)
        balance_timeseries_df = pd.DataFrame(balance_history).round(2)

        return trades_df, balance_timeseries_df, summary
