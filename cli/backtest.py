import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from yahoo_fin import stock_info
import datetime as dt
import matplotlib.ticker as plticker
import numpy as np

from backtest_state import IS_LONG, IS_SHORT, GO_LONG, GO_SHORT, NOT_ENOUGH_DATA
from strategy_3x_neg_3x_with_dma import strategy_3x_neg_3x_with_dma
from strategy_3x_with_dma import strategy_3x_with_dma
from strategy_buy_and_hold import strategy_buy_and_hold
from strategy_3x_with_dma_cash_when_short import strategy_3x_with_dma_cash_when_short

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--limit", type=int)
parser.add_argument("--graph")
args = parser.parse_args()


portfolio_csv_path = f"./../data/backtest/TSLA"
dma_periods = [50, 100, 200, 304]
initial_investment = 100


def calc_is_above_dma(row, dma):
    if dma != None:
        return row.adjclose > dma
    else:
        return NOT_ENOUGH_DATA


def calculate_leverage(price, percent_change, leverage):
    return price * (1 + (percent_change * leverage))


def round2(number):
    return round(number, 2)


def change_state(current_state, is_above_dma, date=None):
    if is_above_dma == NOT_ENOUGH_DATA:
        return NOT_ENOUGH_DATA

    if is_above_dma == True:
        if current_state == IS_SHORT or current_state == NOT_ENOUGH_DATA:
            return GO_LONG
        return IS_LONG

    if is_above_dma == False:
        if current_state == IS_LONG or current_state == NOT_ENOUGH_DATA:
            return GO_SHORT
        return IS_SHORT


def run(strategy_label, strategy, ticker="TSLA"):
    stockDf = None
    csvPath = f"./../data/{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

    try:
        stockDf = pd.read_csv(csvPath)
        print(f"\n[info] Reading from CSV {csvPath}\n")
    except:
        stockDf = stock_info.get_data(ticker)
        stockDf = stockDf.rename_axis("date").reset_index()
        stockDf.to_csv(csvPath)
        print(f"[info] Querying Yahoo Finance and saving to {csvPath}\n")

    portfolio = pd.DataFrame(
        data={
            "date": ["start"],
            "tsla_price": [stockDf["adjclose"].iloc[0]],
            "dma": [0],
            "tsla": [initial_investment / stockDf["adjclose"].iloc[0]],
            "3x": [0],
            "-3x": [0],
            "cash_balance": [0],
            "total_value": [initial_investment],
            "state": [NOT_ENOUGH_DATA],
        }
    )

    for dma_period in dma_periods:
        index = 0
        data = stockDf[-1250:]
        price_3x_long = 100
        price_3x_short = 100
        current_state = NOT_ENOUGH_DATA
        comparison_price = None
        portfolios = []

        for row in data.itertuples():
            previous_data = stockDf[:index]
            previous_tsla_count = portfolio["tsla"].iloc[-1]
            previous_3x_count = portfolio["3x"].iloc[-1]
            previous_neg_3x_count = portfolio["-3x"].iloc[-1]
            todays_close = round2(row.adjclose)
            cash_balance = portfolio["cash_balance"].iloc[-1]

            if index >= 1:
                comparison_price = round2(data.iloc[index - 1]["adjclose"])

            percent_change = 0
            if comparison_price != None:
                percent_change = (todays_close / comparison_price) - 1

            price_3x_long = calculate_leverage(price_3x_long, percent_change, 3)
            price_3x_short = calculate_leverage(price_3x_short, percent_change, -3)

            dma_series = previous_data["adjclose"].rolling(dma_period).mean()[-1:]

            dma = None
            if not dma_series.isna().all():
                dma = round(dma_series.values[0], 2)

            is_above_dma = calc_is_above_dma(row, dma)

            current_state = change_state(current_state, is_above_dma, row.date)

            (
                new_tsla_count,
                new_3x_count,
                new_neg_3x_count,
                cash_balance,
                total_value,
            ) = strategy(
                current_state,
                row,
                price_3x_long,
                price_3x_short,
                previous_tsla_count,
                previous_3x_count,
                previous_neg_3x_count,
                cash_balance,
            )

            portfolio = pd.concat(
                [
                    portfolio,
                    pd.DataFrame(
                        data={
                            "date": [row.date],
                            "tsla_price": [row.adjclose],
                            "dma": [dma],
                            "tsla": [new_tsla_count],
                            "3x": [new_3x_count],
                            "-3x": [new_neg_3x_count],
                            "cash_balance": [cash_balance],
                            "total_value": [total_value],
                            "state": [current_state],
                        }
                    ),
                ],
                join="inner",
            )

            index += 1

        portfolio = portfolio[1:]
        portfolio.round({"tsla": 2, "3x": 2, "-3x": 2, "total_value": 2})
        portfolio.to_csv(f"{portfolio_csv_path}-{strategy_label}-{dma_period}dma.csv")

        print(
            f"[info] Saving portfolio backtest to {portfolio_csv_path}-{strategy_label}-{dma_period}dma.csv\n"
        )

        portfolio["date"] = pd.to_datetime(portfolio["date"], format="%Y-%m-%d")
        portfolios.append(portfolio)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.plot(
            portfolio["date"],
            portfolio["total_value"],
            label=f"{strategy_label}-{dma_period}dma",
        )
        plt.gcf().autofmt_xdate()

    return portfolios


portfolio1 = run("buy and hold", strategy_buy_and_hold)
portfolio2 = run("3x with DMA", strategy_3x_with_dma)
portfolio3 = run(
    "3x with DMA and cash when short", strategy_3x_with_dma_cash_when_short
)
portfolio4 = run("3x and -3x with DMA", strategy_3x_neg_3x_with_dma)

CB91_Blue = "#2CBDFE"
CB91_Green = "#47DBCD"
CB91_Pink = "#F3A0F2"
CB91_Purple = "#9D2EC5"
CB91_Violet = "#661D98"
CB91_Amber = "#F5B14C"


color_list = [
    CB91_Blue,
    CB91_Pink,
    CB91_Green,
    CB91_Amber,
    CB91_Purple,
    CB91_Violet,
    "#DBFF33",
    "#ff0000",
    "#00ff00",
    "#0000ff",
    "#ff3333",
    "#ffff00",
    "#ff6600",
]
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=color_list)

ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.yaxis.set_major_formatter("${x}")

ax.set_title("TSLA Strategies", color=CB91_Blue)
ax.yaxis.set_ticks(
    np.arange(
        0,
        130000,
        # max(
        #     max(portfolio1["total_value"]),
        #     max(portfolio2["total_value"]),
        #     max(portfolio3["total_value"]),
        #     max(portfolio4["total_value"]),
        # ),
        10000,
    )
)

plt.legend()
plt.savefig("./../data/backtest/tsla-strategies.png")
plt.show()
