"""
CSE 163 THA2 - Pandas Version
Functions that process Pokemon data using Pandas.
"""

import pandas as pd


def species_count(data: pd.DataFrame) -> int:
    """Returns the number of unique Pokemon species."""
    return data["name"].nunique()


def max_level(data: pd.DataFrame) -> tuple[str, int]:
    """
    Returns the name and level of the highest-level Pokemon.
    If there is a tie, the first Pokemon is returned.
    """
    index = data["level"].idxmax()
    row = data.loc[index]

    return row["name"], row["level"]


def filter_range(data: pd.DataFrame,
    lower: int,
    upper: int) -> list[str]:
    """
    Returns names of Pokemon whose level is in the range
    [lower, upper).
    """
    filtered = data[
        (data["level"] >= lower) &
        (data["level"] < upper)
    ]

    return list(filtered["name"])


def mean_attack_for_type(data: pd.DataFrame, pokemon_type: str) -> float | None:
    """
    Returns the average attack for a given Pokemon type.
    Returns None if no Pokemon of that type exist.
    """
    filtered = data[
        data["type"].str.lower() == pokemon_type.lower()
    ]

    if filtered.empty:
        return None

    return filtered["atk"].mean()


