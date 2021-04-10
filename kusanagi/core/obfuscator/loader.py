"""This file provides functions to load the obfuscators."""

from typing import List, Dict, Any

from .validator import VALIDATOR
from ...lib.yaml import load as load_yaml
from ...lib.template import get_template_dir


# Available obfuscator files
OBFUSCATORS = ["cmd.yml"]


def _load() -> List[Dict[Any, Any]]:
    """Load available obfuscator."""
    items = []
    for name in OBFUSCATORS:
        path = get_template_dir(["obfuscators", name])
        data = load_yaml(path, VALIDATOR)
        items += data["obfuscators"]
    return items
