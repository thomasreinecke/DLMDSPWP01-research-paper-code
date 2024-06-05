# DLMDSPWP01-research-paper-code

This is the source code supporting the research paper as part of the deliverable for course DLMDSPWP01 at IU University with title "Analyzing the Effectiveness of Technical Indicators in Stock Trading Strategies with Python"

Tthe research topic presented in this paper focuses on the analysis of trading strategy simulations with just a single technical indicator. Specifically, this study seeks to determine if an isolated application of either the RSI or EMA technical indicator to generate BUY and SELL signals can outperform a Buy-and-Hold strategy using time series data from S&P 500 stocks. 

The code provide 3 main elements:
- a set of functions implemented in python that build the Data acqusition pipeline
- an abstract class ```Analysis``` and specific implementations for the RSI- and EMA-based trading strategies
- a Jupyter notebook ```analysis.ipynb``` that provides data inspection, visualization, single- and multi-stock trading system execution, result extraction and visualization

## Install
install the dependencies in a python virtual environment (you need to have python installed)
```
make
```

gather the data from the public sources, postprocess it and store it locally in a SQLLite db
```
make data
```

## Use the Jupyter Notebook to calculate the trading strategies

```analysis.ipynb```

## Datasources

* List of S&P500 stocks
  https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks
* Timeseries data imported from Yahoo Finance (via yfinance module)
