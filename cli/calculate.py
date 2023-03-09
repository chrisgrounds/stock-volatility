import pandas as pd


def calculate(data, days, limit=None):
    volatilityMeasurements = []
    comparisonPrice = None
    currentRow = 0

    dataRange = data[-limit:] if limit else data

    for _, row in dataRange.iterrows():
        if currentRow >= days:
            comparisonPrice = dataRange.iloc[currentRow - days]["adjclose"]

        currentDaysPrice = row.adjclose

        if comparisonPrice != None:
            percentChange = 100 * ((currentDaysPrice / comparisonPrice) - 1)

            volatilityMeasurements.append(
                {"date": row["date"], "percent_change": percentChange}
            )

        currentRow += 1

    return pd.DataFrame(volatilityMeasurements)
