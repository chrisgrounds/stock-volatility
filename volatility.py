
import pandas as pd
from datetime import datetime

from yahoo_fin import stock_info

ticker = "TSLA"

csvPath = f"./{ticker}-{datetime.today().strftime('%Y-%m-%d')}.csv"

stockDf = None

try:
    stockDf = pd.read_csv(csvPath)
    print(f"Reading from CSV {csvPath}\n")
except:
    stockDf = stock_info.get_data(ticker)
    stockDf.to_csv(csvPath)
    print(f"Querying Yahoo Finance and saving to {csvPath}\n")


def calculateChanges(days):
    volatilityMeasurements = []
    comparisonPrice = None
    currentRow = 0

    for date, row in stockDf.iterrows():
        currentDaysPrice = row["adjclose"]

        if (comparisonPrice != None):
            diff = abs(currentDaysPrice - comparisonPrice)
            percentChange = round((diff / currentDaysPrice) * 100, 2)
            volatilityMeasurements.append(
                {"date": date, "percent_change": percentChange})

        if (currentRow >= days):
            comparisonPrice = stockDf.iloc[currentRow - days]["adjclose"]

        currentRow += 1

    return pd.DataFrame(volatilityMeasurements)[-180:]


dailyPercentChanges = [x for x in calculateChanges(1)["percent_change"]]
weeklyPercentChanges = [x for x in calculateChanges(7)["percent_change"]]
monthlyPercentChanges = [x for x in calculateChanges(30)["percent_change"]]

dailyAvgPercentChange = round(
    sum(dailyPercentChanges) / len(dailyPercentChanges), 2)
weeklyAvgPercentChange = round(
    sum(weeklyPercentChanges) / len(weeklyPercentChanges), 2)
monthlyAvgPercentChange = round(
    sum(monthlyPercentChanges) / len(monthlyPercentChanges), 2)


print(calculateChanges(30))
print(f"{ticker} Daily volatility: {dailyAvgPercentChange}%")
print(f"{ticker} Weekly volatility: {weeklyAvgPercentChange}%")
print(f"{ticker} Monthly volatility: {monthlyAvgPercentChange}%")
