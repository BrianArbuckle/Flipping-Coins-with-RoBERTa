# imports

import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt

__author__ = "Brian Arbuckle, Benu Atri and Paras Jamil"
__version__ = "CS224u, Final Project 2021 v1"


def get_stock_prices(
	tickers: list, start: str, end: str, pause: float = 0.5
) -> pd.DataFrame:
	"""
	Returns stock open, close and adjusted close prices (low, high and volume 
	are dropped) from yahoo finance from a list of ticker symbols for the given 
	start and end dates. 

	Args:
		tickers (list): A list of symbols, as strings such as:
			tickers = ['AAPL', 'TSLA', 'ZM']
		start (str): Start date for retreaving ticker symbol price data
			in the "year-mo-da" 2021-02-28 format dt.strftime('%Y-%m-%d')
		end (str): End date for retreaving ticker symbol price data
			in the "year-mo-da" 2021-02-28 format dt.strftime('%Y-%m-%d')
		pause (float): The pandas datareader in conjection with yahoo 
			tend to timeout when there are too many consecutive requests.
	Returns:
		pd.DataFrame: as a multi-index dataframe.
	"""

	df = pdr.get_data_yahoo(tickers, start=start, end=end, pause=0.5)
	df.fillna(method="bfill", inplace=True)

	df.drop(["Low", "High", "Volume"], axis=1, level=0, inplace=True)
	df.rename(
		columns={"Adj Close": "adj_close", "Close": "close", "Open": "open"},
		level=0,
		inplace=True,
	)
	# df.reindex(columns = df.columns.reindex(['open', 'close', 'adj_close'], level = 0)[0] inplace=True)

	return df


def performance_classifier(
	open_date: str,
	close_date: str,
	ticker: str,
	benchmark: str,
	stocks_df: pd.DataFrame,
	benchmark_df: pd.DataFrame
	) -> int:

	"""	
	Returns a binary classification label for a stock price, compared to the 
	underlying benchmark over a given period of time. If the stock performs 
	better than the benchmark, the function returns 1 or 0 when it underperforms 
	the benchmark.

	Args:
		open_date (str): This is the date for the stock opening price after an 
			earnings announcement.
		close_date (str): This is the date for the stock closing price before an 
			earnings announcement. 
		ticker (str): The ticker symbol for the stock being classified.
		benchmark (str): The ticker symbol for the benchmark for comparison.
		stocks_df (pd.DataFrame): DataFrame with the stock open and close data.
		benchmark_df (pd.DataFrame): DataFrame with the benchmark open and close 
			data.

	Returns:
		int: The binary classification label.
	"""

	stock_open = stocks_df.loc[open_date, "open"][ticker]
	stock_close_open_day = stocks_df.loc[open_date, "close"][ticker]
	stock_adj_close_open_day = stocks_df.loc[open_date, "adj_close"][ticker]
	stock_adj_close = stocks_df.loc[close_date, "adj_close"][ticker]
	stock_adj_open = (stock_open / stock_close_open_day) * stock_adj_close_open_day

	stock_performance = stock_adj_close / stock_adj_open

	bench_open = benchmark_df.loc[open_date, "open"][benchmark]
	bench_close_open_day = benchmark_df.loc[open_date, "close"][benchmark]
	bench_adj_close_open_day = benchmark_df.loc[open_date, "adj_close"][benchmark]
	bench_adj_close = benchmark_df.loc[close_date, "adj_close"][benchmark]
	bench_adj_open = (bench_open / bench_close_open_day) * bench_adj_close_open_day

	benchmark_performance = bench_adj_close / bench_adj_open

	result = stock_performance - benchmark_performance
	performance_label = 1 if result >= 0 else 0
	return int(performance_label), result


def next_trading_day(day: dt.datetime, benchmark_df_index: pd.array, forward:bool = True) -> dt.datetime:

	"""
	Since this strategey uses the assumption that a buy or sell order 
	will be placed after the financial report is ordered. 

	Args:
		day (dt.datetime): [description]
		benchmark_df_index (pd.array): [description]
		forward (bool): This setting looks for the next trading day (default True). 
			When set to False, it looks for the previous trading day. 

	Returns:
		[type]: [description]
	"""
	for i in range(1, 6):
		if forward == False:
			day = day - dt.timedelta(i)
		else:
			day = day + dt.timedelta(i)
		if day in benchmark_df_index:
			return day
	return pd.NaT

def get_close_date(varA: dt.datetime, varB: list, threshold: int = 21) -> dt.datetime:
    diff = [x-varA for x in varB]
    diff = [y+dt.timedelta(10000) if y < dt.timedelta(0) else y for y in diff]
    if len(diff) > 0: 
        best = min(diff)
        if best < dt.timedelta(threshold):
            return varB[diff.index(best)]
        else:
            return None
    else:
        return None

def get_cik_codes(cik_file):
    """From FinnBert"""
    cik_codes = []
    with open(cik_file, newline='') as csvfile:
        cik_reader = csv.reader(csvfile, delimiter='|', )
        next(cik_reader, None)  # skip the headers
        for row in cik_reader:
            cik_codes.append(row[0])
    return cik_codes
