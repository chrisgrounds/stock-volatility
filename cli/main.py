import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
from yahoo_fin import stock_info
import math

from calculate import calculate
from average import average
from ui import render
from get_percent_change import get_percent_change
from std_dev import std_dev
from moving_average import moving_average

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--limit", type=int)
parser.add_argument("--graph")
args = parser.parse_args()

ticker = args.ticker
limit = args.limit
graph = args.graph


def format_emoji(x):
    if x == True:
        return "✔️"
    else:
        return "❌"


def to_lev_or_not_to_lev(
    weekly_vol_annualised,
    stock_price,
    ma_200,
    index_weekly_vol_annualised,
    index_stock_price,
    index_ma_200,
):
    print("\n-- Leverage Decision Maker --")

    index_vol_annualised_below_40 = index_weekly_vol_annualised > 40
    index_above_ma_200 = index_stock_price > index_ma_200

    # TODO: find relevant historical figure for ticker/tsla
    vol_annualised_below_40 = weekly_vol_annualised > 40
    above_ma_200 = stock_price > ma_200

    print(
        "index_vol_annualised_below_40: ", format_emoji(index_vol_annualised_below_40)
    )
    print("index_above_ma_200: ", format_emoji(index_above_ma_200))
    print("vol_annualised_below_40: ", format_emoji(vol_annualised_below_40))
    print("above_ma_200: ", format_emoji(above_ma_200))

    return weekly_vol_annualised < 40 and stock_price > ma_200


def run(ticker):
    csvPath = f"./../data/{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

    stockDf = None

    try:
        stockDf = pd.read_csv(csvPath)
        print(f"Reading from CSV {csvPath}\n")
    except:
        stockDf = stock_info.get_data(ticker)
        stockDf = stockDf.rename_axis("date").reset_index()
        stockDf.to_csv(csvPath)
        print(f"Querying Yahoo Finance and saving to {csvPath}\n")

    stock_price = stockDf["adjclose"][-1:].values[0]
    print("The price as of last close: " + str(stock_price))

    # TODO: Just merge this into stockDf
    dailyChanges = calculate(stockDf, 1, limit)
    sorteddailyChanges = dailyChanges.sort_values(by=["percent_change"])
    largestDailyChange = sorteddailyChanges.iloc[-1]

    daily_mean_change = get_percent_change(dailyChanges)
    weekly_mean_change = get_percent_change(calculate(stockDf, 5, limit))
    monthly_mean_change = get_percent_change(calculate(stockDf, 20, limit))

    daily_std_dev = std_dev(daily_mean_change)
    weekly_std_dev = std_dev(weekly_mean_change)
    monthly_std_dev = std_dev(monthly_mean_change)

    num_trading_days = 252
    num_weeks = 52
    num_months = 12
    daily_vol_annualised = daily_std_dev * math.sqrt(num_trading_days)
    weekly_vol_annualised = weekly_std_dev * math.sqrt(num_weeks)
    monthly_vol_annualised = monthly_std_dev * math.sqrt(num_months)

    sigma_move = round(
        (largestDailyChange["percent_change"] - average(daily_mean_change))
        / daily_std_dev,
        2,
    )

    print(sorteddailyChanges)

    render(
        ticker=ticker,
        daily=average(daily_mean_change),
        weekly=average(weekly_mean_change),
        monthly=average(monthly_mean_change),
        daily_std_dev=daily_std_dev,
        weekly_std_dev=weekly_std_dev,
        monthly_std_dev=monthly_std_dev,
    )

    print(
        "The largest daily change was "
        + str(largestDailyChange["percent_change"])
        + "% on "
        + str(
            largestDailyChange["date"]
            + " which was a "
            + str(sigma_move)
            + " sigma move"
        )
    )

    axarr = dailyChanges.hist(
        column="percent_change",
        bins=100,
        grid=False,
        figsize=(12, 8),
        color="#86bf91",
        zorder=2,
        rwidth=0.9,
    )

    for ax in axarr.flatten():
        ax.set_title("Daily Volatility over the last " + str(limit) + " days")
        ax.set_xlabel("Daily % Volatility")
        ax.set_ylabel("Frequency")

    ma_50 = moving_average(stockDf, 50)["MA 50"]
    ma_200 = moving_average(stockDf, 200)["MA 200"]

    print("\n50 day moving average: " + str(ma_50[-1:].values[0]))
    print("200 day moving average: " + str(ma_200[-1:].values[0]))

    print("\nAnnualised daily volatility: " + str(daily_vol_annualised))
    print("Annualised weekly volatility: " + str(weekly_vol_annualised))
    print("Annualised monthly volatility: " + str(monthly_vol_annualised))

    return weekly_vol_annualised, stock_price, ma_200[-1:].values[0]


weekly_vol_annualised, stock_price, ma_200 = run(ticker)
index_weekly_vol_annualised, index_stock_price, index_ma_200 = run("SPY")

to_lev_or_not_to_lev(
    weekly_vol_annualised,
    stock_price,
    ma_200,
    index_weekly_vol_annualised,
    index_stock_price,
    index_ma_200,
)

if graph:
    plt.show()
