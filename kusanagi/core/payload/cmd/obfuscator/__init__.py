"""Obfuscator module."""
from typing import List, Dict, Any
import copy

from .validator import VALIDATOR
from ....loader import load

# Available obfuscator files
OBFUSCATOR_FILES = [
    "bash-gnu.yml",
]

OBFUSCATOR_SUBDIRS = ["cmd", "obfuscators"]


def get_obfuscators() -> List[Dict[str, Any]]:
    """Returns list of unparsed obfuscators."""
    return load(OBFUSCATOR_FILES, OBFUSCATOR_SUBDIRS, VALIDATOR)
