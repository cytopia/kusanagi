"""This module provides helper functions."""

from typing import List


def intersect(list1: List[str], list2: List[str]) -> List[str]:
    """Returns the intersection of two lists of strings."""
    return list(set(list1) & set(list2))


def unique(list1: List[str]) -> List[str]:
    """Returns a list with unique items."""
    return list(set(list1))
