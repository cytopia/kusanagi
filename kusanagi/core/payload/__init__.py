"""Payload module."""
from typing import List, Dict, Any
from ..filter import *
from ..sorter import *


def filter_items(items: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Returns filtered item list.

    Args:
        items: The items to filter.
        filters: The filter settings.

    Returns:
        List[dict]: List of filtered payload items.
    """
    if "exe" in filters:
        items = filter_executables(items, filters["exe"])
    if "lang" in filters:
        items = filter_languages(items, filters["lang"])
    if "shells" in filters:
        items = filter_shells(items, filters["shells"])
    if "os" in filters:
        items = filter_os(items, filters["os"])
    if "badchars" in filters:
        items = filter_badchars(items, filters["badchars"])
    if "maxlen" in filters:
        items = filter_maxlen(items, filters["maxlen"])
    return items


def sort_items(items: List[Dict[str, Any]], sort: str) -> List[Dict[str, Any]]:
    """Return sorted item list.

    Args:
        items: The items to sort.
        sort: What method to sort by (default, rating, length).

    Returns:
        List[dict]: List of sorted payload items.
    """
    if sort == "rating":
        return sort_by_rating(items)
    if sort == "length":
        return sort_by_length(items)
    return sort_by_default(items)


# def encode_items(items: List[dict], encoders: List[str]) -> List[dict]:
#     """Return payload items with encoded output item[x]["encoded"].
#
#     Args:
#         items: The items to encode (add "encoded" key to).
#         encoders: List of encoder function names.
#
#     Returns:
#         List[dict]: List of items with additional "encoded" key added.
#     """
#     for i, _ in enumerate(items):
#         for encoder in encoders:
#             items[i]["encoded"] = encode(items[i]["payload"], encoder)
#     return items
