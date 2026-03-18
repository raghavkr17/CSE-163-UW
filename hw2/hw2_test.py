"""
CSE 163 THA2 Tests
Tests for both manual and pandas implementations.
"""

import pandas as pd
from cse163_utils import parse

import hw2_manual
import hw2_pandas

SPEC_TEST_FILE = "pokemon_test.csv"


def test_species_count() -> None:
    """Tests species_count."""
    data = parse(SPEC_TEST_FILE)
    df = pd.read_csv(SPEC_TEST_FILE)

    assert hw2_manual.species_count(data) == 3
    assert hw2_pandas.species_count(df) == 3


def test_max_level() -> None:
    """Tests max_level."""
    data = parse(SPEC_TEST_FILE)
    df = pd.read_csv(SPEC_TEST_FILE)

    assert hw2_manual.max_level(data) == ("Lapras", 72)
    assert hw2_pandas.max_level(df) == ("Lapras", 72)


def test_filter_range() -> None:
    """Tests filter_range."""
    data = parse(SPEC_TEST_FILE)
    df = pd.read_csv(SPEC_TEST_FILE)

    expected = ["Arcanine", "Arcanine", "Starmie"]

    assert hw2_manual.filter_range(data, 35, 72) == expected
    assert hw2_pandas.filter_range(df, 35, 72) == expected


def test_mean_attack_for_type() -> None:
    """Tests mean_attack_for_type."""
    data = parse(SPEC_TEST_FILE)
    df = pd.read_csv(SPEC_TEST_FILE)

    assert hw2_manual.mean_attack_for_type(data, "fire") == 47.5
    assert hw2_pandas.mean_attack_for_type(df, "fire") == 47.5


def main() -> None:
    """Runs all test functions."""
    test_species_count()
    test_max_level()
    test_filter_range()
    test_mean_attack_for_type()
    print("All tests passed!")


if __name__ == "__main__":
    main()
