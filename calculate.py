import pandas as pd


def calculate(data, days):
    volatilityMeasurements = []
    comparisonPrice = None
    currentRow = 0

    for date, row in data.iterrows():
        currentDaysPrice = row["adjclose"]

        if (comparisonPrice != None):
            diff = abs(currentDaysPrice - comparisonPrice)
            percentChange = round((diff / currentDaysPrice) * 100, 2)
            volatilityMeasurements.append(
                {"date": date, "percent_change": percentChange})

        if (currentRow >= days):
            comparisonPrice = data.iloc[currentRow - days]["adjclose"]

        currentRow += 1

    return pd.DataFrame(volatilityMeasurements)[-180:]
