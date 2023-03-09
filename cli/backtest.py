import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from yahoo_fin import stock_info
import datetime as dt

from backtest_state import IS_LONG, IS_SHORT, GO_LONG, GO_SHORT, NOT_ENOUGH_DATA
from strategy_3x_neg_3x_with_dma import strategy_3x_neg_3x_with_dma
from strategy_3x_with_dma import strategy_3x_with_dma
from strategy_buy_and_hold import strategy_buy_and_hold

parser = argparse.ArgumentParser()
parser.add_argument("--ticker")
parser.add_argument("--limit", type=int)
parser.add_argument("--graph")
args = parser.parse_args()


portfolio_csv_path = f"./../data/backtest/TSLA.csv"
dma_period = 304
initial_investment = 100


def calc_is_above_dma(row, dma):
    if dma != None:
        return row["adjclose"] > dma
    else:
        return NOT_ENOUGH_DATA


def calculate_leverage(price, percent_change, leverage):
    return price * (1 + (percent_change * leverage))


def change_state(current_state, is_above_dma):
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
            "total_value": [initial_investment],
            "state": [NOT_ENOUGH_DATA],
        }
    )

    price_3x_long = 100
    price_3x_short = 100

    for index, row in stockDf.iterrows():
        previous_data = stockDf[:index]
        previous_tsla_count = portfolio["tsla"].iloc[-1]
        previous_3x_count = portfolio["3x"].iloc[-1]
        previous_neg_3x_count = portfolio["-3x"].iloc[-1]
        todays_close = row["adjclose"]
        comparison_price = None
        current_state = NOT_ENOUGH_DATA

        if index >= 1:
            comparison_price = stockDf.iloc[index - 1]["adjclose"]

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

        current_state = change_state(current_state, is_above_dma)

        (
            new_tsla_count,
            new_3x_count,
            new_neg_3x_count,
            total_value,
        ) = strategy(
            current_state,
            row,
            price_3x_long,
            price_3x_short,
            previous_tsla_count,
            previous_3x_count,
            previous_neg_3x_count,
        )

        portfolio = pd.concat(
            [
                portfolio,
                pd.DataFrame(
                    data={
                        # "date": [dt.datetime.strptime(row["date"], "%Y-%m-%d")],
                        "date": [row["date"]],
                        "tsla_price": [row["adjclose"]],
                        "dma": [dma],
                        "tsla": [new_tsla_count],
                        "3x": [new_3x_count],
                        "-3x": [new_neg_3x_count],
                        "total_value": [total_value],
                        "state": [current_state],
                    }
                ),
            ],
            join="inner",
        )

    portfolio = portfolio[1:]
    portfolio.round({"tsla": 2, "3x": 2, "-3x": 2, "total_value": 2})
    portfolio.to_csv(f"{portfolio_csv_path}-{strategy_label}.csv")

    print(
        f"[info] Saving portfolio backtest to {portfolio_csv_path}-{strategy_label}.csv\n"
    )

    portfolio["date"] = pd.to_datetime(portfolio["date"], format="%Y-%m-%d")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.plot(portfolio["date"], portfolio["total_value"], label=strategy_label)
    plt.gcf().autofmt_xdate()


run("buy and hold", strategy_buy_and_hold)
run("3x with DMA", strategy_3x_with_dma)
run("3x and -3x with DMA", strategy_3x_neg_3x_with_dma)


for ax in plt.gcf().axes:
    ax.set_title("TSLA Strategies", color="C0")
    ax.get_lines()[0].set_color("#4C4CB2")
    ax.get_lines()[1].set_color("#fcba03")
    ax.get_lines()[2].set_color("#3FBFBF")

plt.legend()
plt.show()
