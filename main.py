import pandas as pd
import sys
from datetime import datetime

from yahoo_fin import stock_info

from calculate import calculate
from average import average
from ui import render
from get_percent_change import get_percent_change
from std_dev import std_dev

ticker = sys.argv[1]

csvPath = f"./data/{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

stockDf = None

try:
    stockDf = pd.read_csv(csvPath)
    print(f"Reading from CSV {csvPath}\n")
except:
    stockDf = stock_info.get_data(ticker)
    stockDf.to_csv(csvPath)
    print(f"Querying Yahoo Finance and saving to {csvPath}\n")

daily_vols = get_percent_change(calculate(stockDf, 1))
weekly_vols = get_percent_change(calculate(stockDf, 7))
monthly_vols = get_percent_change(calculate(stockDf, 30))

daily_std_dev = std_dev(daily_vols)
weekly_std_dev = std_dev(weekly_vols)
monthly_std_dev = std_dev(monthly_vols)

print(calculate(stockDf, 1))

render(ticker=ticker, daily=average(daily_vols), weekly=average(
    weekly_vols), monthly=average(monthly_vols), daily_std_dev=daily_std_dev, 
    weekly_std_dev=weekly_std_dev, monthly_std_dev=monthly_std_dev)
