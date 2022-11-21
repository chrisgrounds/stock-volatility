def render(ticker, daily=0, weekly=0, monthly=0, daily_std_dev=0, weekly_std_dev=0, monthly_std_dev=0):
    print(f"{ticker} Daily volatility: {daily}%")
    print(f"{ticker} Weekly volatility: {weekly}%")
    print(f"{ticker} Monthly volatility: {monthly}%")

    print("\n")
    print("Standard Deviation")
    print("(68%, 95%, 99.7%)")
    print(f"Daily. 1σ: {daily_std_dev}%, 2σ: {round(daily_std_dev * 2, 2)}%, 3σ: {round(daily_std_dev * 3, 2)}%")
    print(f"Weekly. 1σ: {weekly_std_dev}%, 2σ: {round(weekly_std_dev * 2, 2)}%, 3σ: {round(weekly_std_dev * 3, 2)}%")
    print(f"Monthly. 1σ: {monthly_std_dev}%, 2σ: {round(monthly_std_dev * 2, 2)}%, 3σ: {round(monthly_std_dev * 3, 2)}%")
