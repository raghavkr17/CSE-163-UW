"""
Hunter Schafer
CSE 163 AX

A file that contains some CSE 163 specific helper functions
You do not need to understand how these functions are implemented,
but you should be able to use the ones we described in class!
"""

import pandas as pd

from typing import TypedDict

TOLERANCE = 0.001

Pokemon = TypedDict('Pokemon', {
    "id": int,
    "name": str,
    "level": int,
    "personality": str,
    "type": str,
    "weakness": str,
    "atk": int,
    "def": int,
    "hp": int,
    "stage": int,
})


def parse(file_name: str) -> list[Pokemon]:
    """
    Reads the CSV with the given file_name and returns it as a list of
    dictionaries. The list will have a dictionary for each row, and each
    dictionary will have a key for each column.
    """
    df = pd.read_csv(file_name)
    return df.to_dict('records')
