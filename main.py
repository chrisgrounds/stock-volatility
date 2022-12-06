import pandas as pd
from datetime import datetime
import argparse

from yahoo_fin import stock_info

from calculate import calculate
from average import average
from ui import render
from get_percent_change import get_percent_change
from std_dev import std_dev
# from update_reddit_flair import update_reddit_flair
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--limit", type=int)
args = parser.parse_args()

ticker = args.ticker
limit = args.limit

csvPath = f"./data/{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

stockDf = None

try:
    stockDf = pd.read_csv(csvPath)
    print(f"Reading from CSV {csvPath}\n")
except:
    stockDf = stock_info.get_data(ticker)
    stockDf.to_csv(csvPath)
    print(f"Querying Yahoo Finance and saving to {csvPath}\n")

dailyChanges = calculate(stockDf, 1, limit)
sorteddailyChanges = dailyChanges.sort_values(by=['percent_change'])
largestDailyChange = sorteddailyChanges.iloc[-1]

daily_vols = get_percent_change(dailyChanges)
weekly_vols = get_percent_change(calculate(stockDf, 5, limit))
monthly_vols = get_percent_change(calculate(stockDf, 20, limit))

daily_std_dev = std_dev(daily_vols)
weekly_std_dev = std_dev(weekly_vols)
monthly_std_dev = std_dev(monthly_vols)

sigma_move = round((largestDailyChange["percent_change"] - average(daily_vols)) / daily_std_dev, 2)

print(sorteddailyChanges)

render(ticker=ticker, daily=average(daily_vols), weekly=average(
    weekly_vols), monthly=average(monthly_vols), daily_std_dev=daily_std_dev, 
    weekly_std_dev=weekly_std_dev, monthly_std_dev=monthly_std_dev)

print("The largest daily change was " + str(largestDailyChange["percent_change"]) + "% on " + str(largestDailyChange['date'] + " which was a " + str(sigma_move) + " sigma move"))

axarr = dailyChanges.hist(column='percent_change', bins=100, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)

for ax in axarr.flatten():
    ax.set_title("Daily Volatility over the last " + str(limit) + " days")
    ax.set_xlabel("Daily % Volatility")
    ax.set_ylabel("Frequency")

plt.show()

# https://arxiv.org/pdf/1103.5672.pdf#:~:text=a%204%2Dsigma%20event%20is,in%20126%20years%20(!)%3B&text=a%205%2Dsigma%20event%20is,every%2013%2C932%20years(!!)
# k Probability in any given day Expected occurrence: once in every
# 3 0.135% 740.8 days
# 4 0.00317% 31559.6 days
# 5 0.000029% 3,483,046.3 days
# 6 0.000000099% 1,009,976,678 days
# 7 0.000000000129% 7.76e+11 days 

# a 3-sigma event is to be expected about every 741 days or about 1 trading day
# in every three years;
# • a 4-sigma event is to be expected about every 31,560 days or about 1 trading
# day in 126 years (!);
# • a 5-sigma event is to be expected every 3,483,046 days or about 1 day every
# 13,932 years(!!)
# • a 6-sigma event is to be expected every 1,009,976,678 days or about 1 day
# every 4,039,906 years;
# • a 7-sigma event is to be expected every 7.76e+11 days – the number of zero
# digits is so large that Excel now reports the number of days using scientific
# notation, and this number is to be interpreted as 7.76 days with decimal point
# pushed back 11 places. This frequency corresponds to 1 day in 3,105,395,365
# years.