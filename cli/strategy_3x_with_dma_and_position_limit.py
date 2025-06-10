from backtest_state import IS_LONG, IS_SHORT, GO_LONG, GO_SHORT, NOT_ENOUGH_DATA


def strategy_3x_with_dma_and_position_limit(
    current_state,
    row,
    price_3x_long,
    price_3x_short,
    previous_tsla_count,
    previous_3x_count,
    previous_neg_3x_count,
    cash_balance,
):
    total_value = (
        previous_tsla_count * row.adjclose
        + previous_3x_count * price_3x_long
        + previous_neg_3x_count * price_3x_short
    )
    
    if current_state == GO_LONG:
        new_tsla_count = 0
        new_3x_count = min(total_value / price_3x_long, 20000 / price_3x_long)
        new_neg_3x_count = 0
        cash_balance += total_value - (new_3x_count * price_3x_long)
    elif current_state == GO_SHORT:
        new_tsla_count = total_value / row.adjclose
        new_3x_count = 0
        new_neg_3x_count = 0
    else:
        new_tsla_count = previous_tsla_count
        new_3x_count = previous_3x_count
        new_neg_3x_count = previous_neg_3x_count

    return new_tsla_count, new_3x_count, new_neg_3x_count, cash_balance, total_value 