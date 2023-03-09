from backtest_state import IS_LONG, IS_SHORT, GO_LONG, GO_SHORT, NOT_ENOUGH_DATA


def strategy_buy_and_hold(
    current_state,
    row,
    price_3x_long,
    price_3x_short,
    previous_tsla_count,
    previous_3x_count,
    previous_neg_3x_count,
):
    total_value = (
        previous_tsla_count * row["adjclose"]
        + previous_3x_count * price_3x_long
        + previous_neg_3x_count * price_3x_short
    )
    new_tsla_count = previous_tsla_count
    new_3x_count = previous_3x_count
    new_neg_3x_count = previous_neg_3x_count

    return new_tsla_count, new_3x_count, new_neg_3x_count, total_value
