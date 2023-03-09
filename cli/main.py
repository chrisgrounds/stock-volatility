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
from lev import to_lev_or_not_to_lev

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--limit", type=int)
parser.add_argument("--graph")
args = parser.parse_args()

ticker = args.ticker
limit = args.limit
graph = args.graph


def run(ticker):
    stockDf = None
    csvPath = f"./../data/{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

    try:
        stockDf = pd.read_csv(csvPath)
        print(f"\n[info] Reading from CSV {csvPath}\n")
    except:
        stockDf = stock_info.get_data(ticker)
        stockDf = stockDf.rename_axis("date").reset_index()
        stockDf.to_csv(csvPath)
        print(f"[---] Querying Yahoo Finance and saving to {csvPath}\n")

    stock_price = stock_info.get_live_price(ticker)
    print(f"[{ticker}] Price: ${str(round(stock_price, 2))}")

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
    daily_vol_annualised = round(daily_std_dev * math.sqrt(num_trading_days), 2)
    weekly_vol_annualised = round(weekly_std_dev * math.sqrt(num_weeks), 2)
    monthly_vol_annualised = round(monthly_std_dev * math.sqrt(num_months), 2)

    sigma_move = round(
        (largestDailyChange["percent_change"] - average(daily_mean_change))
        / daily_std_dev,
        2,
    )

    render(
        ticker=ticker,
        daily_std_dev=daily_std_dev,
        weekly_std_dev=weekly_std_dev,
        monthly_std_dev=monthly_std_dev,
    )

    print(
        f"[{ticker}] The largest daily change was "
        + str(round(largestDailyChange["percent_change"], 2))
        + "% on "
        + str(largestDailyChange["date"])
        + " which was a "
        + str(sigma_move)
        + " sigma move"
    )

    if graph:
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

    ma_50 = round(moving_average(stockDf, 50)["MA 50"][-1:].values[0], 2)
    ma_200 = round(moving_average(stockDf, 200)["MA 200"][-1:].values[0], 2)
    ma_304 = round(moving_average(stockDf, 304)["MA 304"][-1:].values[0], 2)  # 10 month

    print(f"\n[{ticker}] 50 day moving average: {str(ma_50)}")
    print(f"[{ticker}] 200 day moving average: {str(ma_200)}")
    print(f"[{ticker}] 304 day (10 month) moving average: {str(ma_304)}")

    print(f"\n[{ticker}] Annualised daily volatility: {str(daily_vol_annualised)}%")
    print(f"[{ticker}] Annualised weekly volatility: {str(weekly_vol_annualised)}%")
    print(f"[{ticker}] Annualised monthly volatility: {str(monthly_vol_annualised)}%")

    return (weekly_vol_annualised, stock_price, ma_50, ma_200, ma_304)


weekly_vol_annualised, stock_price, ma_50, ma_200, ma_304 = run(ticker)
(
    index_weekly_vol_annualised,
    index_stock_price,
    index_ma_50,
    index_ma_200,
    index_ma_304,
) = run("SPY")

to_lev_or_not_to_lev(
    ticker,
    weekly_vol_annualised,
    stock_price,
    ma_50,
    ma_200,
    ma_304,
    index_weekly_vol_annualised,
    index_stock_price,
    index_ma_50,
    index_ma_200,
    index_ma_304,
)

if graph:
    plt.show()
