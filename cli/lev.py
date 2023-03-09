def format_emoji(x):
    if x == True:
        return "✔️"
    else:
        return "❌"


def to_lev_or_not_to_lev(
    ticker,
    weekly_vol_annualised,
    stock_price,
    ma_50,
    ma_100,
    ma_200,
    ma_304,
    index_weekly_vol_annualised,
    index_stock_price,
    index_ma_50,
    index_ma_100,
    index_ma_200,
    index_ma_304,
):
    print("\n-- Leverage Decision Maker --")

    index_vol_annualised_below_40 = index_weekly_vol_annualised <= 40
    index_above_ma_100 = index_stock_price > index_ma_100
    index_above_ma_200 = index_stock_price > index_ma_200
    index_above_ma_304 = index_stock_price > index_ma_304
    index_crossover_200_50 = index_ma_50 > index_ma_200
    index_crossover_304_50 = index_ma_50 > index_ma_304

    # TODO: find relevant historical figure for ticker/tsla
    vol_annualised_below_40 = weekly_vol_annualised <= 60
    above_ma_100 = stock_price > ma_100
    above_ma_200 = stock_price > ma_200
    above_ma_304 = stock_price > ma_304
    crossover_200_50 = ma_50 > ma_200
    crossover_304_50 = ma_50 > ma_304

    print(
        f"SPY Annualised Vol Below 40: {format_emoji(index_vol_annualised_below_40)}",
    )
    print(
        f"SPY above 100-day MA: {format_emoji(index_above_ma_100)}",
    )
    print(
        f"SPY above 200-day MA: {format_emoji(index_above_ma_200)}",
    )
    print(
        f"SPY above 304-day (10 month) MA: {format_emoji(index_above_ma_304)}",
    )
    print(
        f"SPY 200/50 Crossover (50 MA > 200 MA): {format_emoji(index_crossover_200_50)}",
    )
    print(
        f"SPY 304/50 Crossover (50 MA > 304 MA (10 month)): {format_emoji(index_crossover_304_50)}",
    )
    print(
        f"{ticker} annualised Vol Below 60: {format_emoji(vol_annualised_below_40)}",
    )
    print(
        f"{ticker} above 100-day MA: {format_emoji(above_ma_100)}",
    )
    print(
        f"{ticker} above 200-day MA: {format_emoji(above_ma_200)}",
    )
    print(
        f"{ticker} above 304-day (10 month) MA: {format_emoji(above_ma_304)}",
    )
    print(
        f"{ticker} 200/50 Crossover (50 MA > 200 MA): {format_emoji(crossover_200_50)}",
    )
    print(
        f"{ticker} 304/50 Crossover (50 MA > 304 MA (10 month)): {format_emoji(crossover_304_50)}",
    )
