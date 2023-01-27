import pandas as pd

def calculate(data, days, limit = None):
    volatilityMeasurements = []
    comparisonPrice = None
    currentRow = 0

    dataRange = data[-limit:] if limit else data

    for _, row in dataRange.iterrows():
        if (currentRow >= days):
            comparisonPrice = dataRange.iloc[currentRow - days]["adjclose"]

        currentDaysPrice = row["adjclose"]
        date = row["Unnamed: 0"]

        if (comparisonPrice != None):
            diff = currentDaysPrice - comparisonPrice
            percentChange = round((diff / comparisonPrice) * 100, 2)
            volatilityMeasurements.append(
                { "date": date, "percent_change": percentChange }
            )

        currentRow += 1

    return pd.DataFrame(volatilityMeasurements)
