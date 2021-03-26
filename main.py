
import pandas as pd
import sys
from datetime import datetime

from yahoo_fin import stock_info

from calculate import calculate


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

dailyPercentChanges = [x for x in calculate(stockDf, 1)["percent_change"]]
weeklyPercentChanges = [x for x in calculate(stockDf, 7)["percent_change"]]
monthlyPercentChanges = [x for x in calculate(stockDf, 30)["percent_change"]]

dailyAvgPercentChange = round(
    sum(dailyPercentChanges) / len(dailyPercentChanges), 2)
weeklyAvgPercentChange = round(
    sum(weeklyPercentChanges) / len(weeklyPercentChanges), 2)
monthlyAvgPercentChange = round(
    sum(monthlyPercentChanges) / len(monthlyPercentChanges), 2)


print(calculate(stockDf, 30))
print(f"{ticker} Daily volatility: {dailyAvgPercentChange}%")
print(f"{ticker} Weekly volatility: {weeklyAvgPercentChange}%")
print(f"{ticker} Monthly volatility: {monthlyAvgPercentChange}%")
