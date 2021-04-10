"""Module to compress the payload."""
from typing import Dict, List, Union, Any

import copy
import re
import itertools


def compress(data: str) -> str:
    """Trims whitepaces and newlines from a payload to make it a small as possible."""
    pattern_rgt = r"\s*$"  # Clean left of string
    pattern_lft = r"^\s*"  # Clean right of string
    pattern_all = r"\s\s"  # Two whitespaces in a row
    lines = []
    for line in data.splitlines():
        line = re.sub(pattern_rgt, "", line)
        line = re.sub(pattern_lft, "", line)
        line = re.sub(pattern_all, " ", line)
        lines.append(line)

    temp = "".join(lines)

    # Repeat until not further possible
    if temp != data:
        return compress(temp)
    return temp
