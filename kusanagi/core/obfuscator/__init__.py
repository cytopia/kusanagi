"""Obfuscator Module."""

from typing import List, Dict, Any
from .loader import _load


def get_obfuscators() -> List[Dict[Any, Any]]:
    """Returns list of obfuscators."""
    return _load()
