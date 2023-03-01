def render(
    ticker,
    daily_std_dev=0,
    weekly_std_dev=0,
    monthly_std_dev=0,
):
    print(f"\n[{ticker}] Standard deviations (68%, 95%, 99.7%)")
    print(
        f"[{ticker}] Daily 1σ: {daily_std_dev}%, 2σ: {round(daily_std_dev * 2, 2)}%, 3σ: {round(daily_std_dev * 3, 2)}%"
    )
    print(
        f"[{ticker}] Weekly 1σ: {weekly_std_dev}%, 2σ: {round(weekly_std_dev * 2, 2)}%, 3σ: {round(weekly_std_dev * 3, 2)}%"
    )
    print(
        f"[{ticker}] Monthly 1σ: {monthly_std_dev}%, 2σ: {round(monthly_std_dev * 2, 2)}%, 3σ: {round(monthly_std_dev * 3, 2)}%"
    )
