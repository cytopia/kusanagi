"""Module to sort payloads on their given options."""
from typing import List
from ..typing.ds_payload import DsPayload


def sort_by_length(payloads: List[DsPayload]) -> List[DsPayload]:
    """Sort payloads by length."""
    return sorted(payloads, key=lambda k: len(k.payload), reverse=True)
