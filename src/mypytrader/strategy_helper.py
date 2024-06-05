# src/pytrader/strategy_helper.py

import pandas as pd
import sqlite3

# returns the relevant data from SQLite for the given symbol
def get_timeseries_data(symbol: str, start_date: str, end_date: str, db_path: str = 'data/stock_data.db') -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    query = f'''
    SELECT ts.date, ts.close
    FROM timeseries ts
    WHERE ts.symbol = '{symbol}' AND ts.date >= '{start_date}' AND ts.date <= '{end_date}'
    ORDER BY ts.date ASC
    '''
    data = pd.read_sql(query, conn, parse_dates=['date'])
    conn.close()
    data = data.reset_index(drop=True)
    data.set_index('date', inplace=True)
    return data

# given a vectorbt resultset, performance metrics are extracted from the results
def extract_results(pf, data, symbol, start_amount, strategy_name):
    # Calculate performance metrics for the strategy
    end_balance = pf.value().iloc[-1]
    absolute_performance = end_balance - start_amount
    total_percentage_performance = (end_balance / start_amount - 1) * 100
    annual_avg_performance = pf.annualized_return(freq='1D') * 100

    # Calculate performance metrics for the benchmark (buy and hold)
    benchmark_end_balance = data['close'].iloc[-1] / data['close'].iloc[0] * start_amount
    benchmark_absolute_performance = benchmark_end_balance - start_amount
    benchmark_total_percentage_performance = (benchmark_end_balance / start_amount - 1) * 100
    benchmark_annual_avg_performance = ((benchmark_end_balance / start_amount) ** (1 / ((data.index[-1] - data.index[0]).days / 365.25)) - 1) * 100

    # Calculate outperformance factor and check if strategy outperformed the benchmark
    outperformance_factor = total_percentage_performance - benchmark_total_percentage_performance
    is_strategy_more_profitable = total_percentage_performance > benchmark_total_percentage_performance

    # Create a results object
    results = {
        'symbol': symbol,
        'strategy': {
            'name': strategy_name,
            'end_balance': end_balance,
            'absolute_performance': absolute_performance,
            'total_percentage_performance': total_percentage_performance,
            'annual_avg_performance': annual_avg_performance
        },
        'benchmark': {
            'end_balance': benchmark_end_balance,
            'absolute_performance': benchmark_absolute_performance,
            'total_percentage_performance': benchmark_total_percentage_performance,
            'annual_avg_performance': benchmark_annual_avg_performance
        },
        'outperformance_factor': outperformance_factor,
        'is_strategy_more_profitable': is_strategy_more_profitable,
        'pf': pf
    }
    return results


# persists the results of a single stock vectorbt backtesting to SQLite
def persist_strategy_results_for_single_stock(results, db_path: str = 'data/stock_data.db'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Print the results to verify they are being passed correctly

        upsert_query = '''
        INSERT INTO performance (
            symbol, strategy_name, strategy_end_balance, strategy_absolute_performance,
            strategy_total_percentage_performance, strategy_annual_avg_performance,
            benchmark_end_balance, benchmark_absolute_performance, benchmark_total_percentage_performance,
            benchmark_annual_avg_performance, outperformance_factor, is_strategy_more_profitable
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(symbol, strategy_name) DO UPDATE SET
            strategy_end_balance = excluded.strategy_end_balance,
            strategy_absolute_performance = excluded.strategy_absolute_performance,
            strategy_total_percentage_performance = excluded.strategy_total_percentage_performance,
            strategy_annual_avg_performance = excluded.strategy_annual_avg_performance,
            benchmark_end_balance = excluded.benchmark_end_balance,
            benchmark_absolute_performance = excluded.benchmark_absolute_performance,
            benchmark_total_percentage_performance = excluded.benchmark_total_percentage_performance,
            benchmark_annual_avg_performance = excluded.benchmark_annual_avg_performance,
            outperformance_factor = excluded.outperformance_factor,
            is_strategy_more_profitable = excluded.is_strategy_more_profitable;
        '''

        print("Trying to persist:", results['strategy']['name'])
        
        cursor.execute(upsert_query, (
            results['symbol'],
            results['strategy']['name'],
            results['strategy']['end_balance'],
            results['strategy']['absolute_performance'],
            results['strategy']['total_percentage_performance'],
            results['strategy']['annual_avg_performance'],
            results['benchmark']['end_balance'],
            results['benchmark']['absolute_performance'],
            results['benchmark']['total_percentage_performance'],
            results['benchmark']['annual_avg_performance'],
            results['outperformance_factor'],
            results['is_strategy_more_profitable']
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error persisting results: {e}")
