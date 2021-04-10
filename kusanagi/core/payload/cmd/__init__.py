"""Payload Module."""

from typing import List, Dict, Any
from .loader import _load
from ...typing.ds_payload import DsPayload


def get_payloads(addr: str, port: str) -> List[DsPayload]:
    """Returns list of payloads."""
    placeholders = {
        "__ADDR__": addr,
        "__PORT__": port,
    }
    return _load(placeholders)
