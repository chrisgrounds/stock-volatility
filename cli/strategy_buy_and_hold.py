from backtest_state import IS_LONG, IS_SHORT, GO_LONG, GO_SHORT, NOT_ENOUGH_DATA


def strategy_buy_and_hold(
    current_state,
    row,
    price_3x_long,
    price_3x_short,
    previous_tsla_count,
    previous_3x_count,
    previous_neg_3x_count,
    cash_balance,
):
    total_value = previous_tsla_count * row.adjclose

    return (
        previous_tsla_count,
        previous_3x_count,
        previous_neg_3x_count,
        cash_balance,
        total_value,
    )
