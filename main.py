
import pandas as pd
import sys
from datetime import datetime

from yahoo_fin import stock_info

from calculate import calculate
from average import average
from ui import render
from get_percent_change import get_percent_change


ticker = sys.argv[1]

csvPath = f"./{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

stockDf = None

try:
    stockDf = pd.read_csv(csvPath)
    print(f"Reading from CSV {csvPath}\n")
except:
    stockDf = stock_info.get_data(ticker)
    stockDf.to_csv(csvPath)
    print(f"Querying Yahoo Finance and saving to {csvPath}\n")

dailyPercentChanges = get_percent_change(calculate(stockDf, 1))
weeklyPercentChanges = get_percent_change(calculate(stockDf, 7))
monthlyPercentChanges = get_percent_change(calculate(stockDf, 30))

print(calculate(stockDf, 30))

render(ticker=ticker, daily=average(dailyPercentChanges), weekly=average(
    weeklyPercentChanges), monthly=average(monthlyPercentChanges))
