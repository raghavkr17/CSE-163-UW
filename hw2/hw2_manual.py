"""
CSE 163 THA2 - Manual Version
Functions that process Pokemon data without using Pandas.
"""

from cse163_utils import Pokemon


def species_count(data: list[Pokemon]) -> int:
    """Returns the number of unique Pokemon species."""
    names = set()

    for pokemon in data:
        names.add(pokemon["name"])

    return len(names)


def max_level(data: list[Pokemon]) -> tuple[str, int]:
    """
    Returns the name and level of the highest-level Pokemon.
    If there is a tie, the first Pokemon is returned.
    """
    highest = data[0]

    for pokemon in data:
        if pokemon["level"] > highest["level"]:
            highest = pokemon

    return highest["name"], highest["level"]


def filter_range(data: list[Pokemon],
    lower: int,
    upper: int) -> list[str]:
    """
    Returns names of Pokemon whose level is in the range
    [lower, upper).
    """
    result = []

    for pokemon in data:
        if lower <= pokemon["level"] < upper:
            result.append(pokemon["name"])

    return result


def mean_attack_for_type(data: list[Pokemon], pokemon_type: str) -> float | None:
    """
    Returns the average attack for a given Pokemon type.
    Returns None if no Pokemon of that type exist.
    """
    total = 0
    count = 0

    for pokemon in data:
        if pokemon["type"].lower() == pokemon_type.lower():
            total += pokemon["atk"]
            count += 1

    if count == 0:
        return None

    return total / count

