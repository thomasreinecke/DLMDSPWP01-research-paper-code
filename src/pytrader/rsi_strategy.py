# src/pytrader/rsi_strategy.py
import pandas as pd
import ta
from .trading_strategy import TradingStrategy

class RSI_Strategy(TradingStrategy):
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30

    def calculate_trades(self, symbol: str, data: pd.DataFrame, start_amount: float):
        cash = start_amount
        positions = {}
        trades = []
        balance_history = []
        current_balance = start_amount

        def balance(current_price):
            invested_capital = sum(position['quantity'] * current_price for position in positions.values())
            return cash + invested_capital

        # Calculate RSI
        data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=14).rsi()

        for i, row in data.iterrows():
            date = row['date']
            rsi = row['RSI']
            close_price = row['close']
            action_taken = False

            # Check for sell signals
            if rsi > self.RSI_OVERBOUGHT and symbol in positions:
                buy_price = positions[symbol]['buy_price']
                quantity = positions[symbol]['quantity']
                entry_amount = positions[symbol]['entry_amount']
                sell_price = close_price
                exit_amount = sell_price * quantity
                profit_loss = exit_amount - entry_amount
                trades.append({
                    'index': len(trades),
                    'symbol': symbol,
                    'entry_amount': entry_amount,
                    'entry_price': buy_price,
                    'entry_date': positions[symbol]['buy_date'],
                    'quantity': quantity,
                    'exit_date': date,
                    'exit_price': sell_price,
                    'pl': profit_loss,
                    'exit_amount': exit_amount
                })
                cash += exit_amount
                del positions[symbol]
                action_taken = True

            # Check for buy signals
            elif rsi < self.RSI_OVERSOLD and cash >= close_price and symbol not in positions:
                quantity = int(cash / close_price)
                entry_amount = close_price * quantity
                positions[symbol] = {
                    'buy_price': close_price,
                    'quantity': quantity,
                    'buy_date': date,
                    'entry_amount': entry_amount
                }
                cash -= entry_amount
                action_taken = True

            current_balance = balance(close_price)
            balance_history.append({'date': date, 'balance': current_balance})

        # Finalize trades and balance history
        if symbol in positions:
            final_date = data['date'].max()
            buy_price = positions[symbol]['buy_price']
            quantity = positions[symbol]['quantity']
            entry_amount = positions[symbol]['entry_amount']
            sell_price = data.loc[data['date'] == final_date, 'close'].values[0]
            exit_amount = sell_price * quantity
            profit_loss = exit_amount - entry_amount
            trades.append({
                'index': len(trades),
                'symbol': symbol,
                'entry_amount': entry_amount,
                'entry_price': buy_price,
                'entry_date': positions[symbol]['buy_date'],
                'quantity': quantity,
                'exit_date': final_date,
                'exit_price': sell_price,
                'pl': profit_loss,
                'exit_amount': exit_amount
            })
            cash += exit_amount
            balance_history.append({'date': final_date, 'balance': balance(sell_price)})

        # Summary of the performance
        total_pl = sum(trade['pl'] for trade in trades)
        total_trades = len(trades)
        profit_trades = sum(1 for trade in trades if trade['pl'] > 0)
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
