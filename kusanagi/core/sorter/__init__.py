"""Module to sort payloads on their given options."""
from typing import List, Dict, Any


def sort_by_default(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort payloads by rating and then length length."""
    return sorted(payloads, key=lambda k: (int(k["rating"]), len(k["payload"])), reverse=True)


def sort_by_length(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort payloads by length."""
    return sorted(payloads, key=lambda k: len(k["payload"]), reverse=True)


def sort_by_rating(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort payloads by rating."""
    return sorted(payloads, key=lambda k: int(k["rating"]), reverse=True)
