from math import floor, ceil

def normal_round(x: float) -> int:
    """Rounds x to the closest integer, ties rounded up."""
    # this function is needed because built-in round() does not work with negative numbers
    # e.g. round(-3.5) == -4    vs.    normal_round(-3.5) == -3

    if ceil(x) - x <= 0.5:
        return ceil(x)
    return floor(x)
