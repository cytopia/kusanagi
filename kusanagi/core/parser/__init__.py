"""Module to parse placeholders and functions that are defined in yaml templates."""

from typing import List, Dict, Any
import re
from .function import run


def parse(items: List[Dict[str, Any]], placeholders: Dict[str, str]) -> List[Dict[str, Any]]:
    """Returns items parsed with placeholders, variables and functions.

    Args:
        items: List of items to parse
        placeholders: placeholders to be replaced in 'payload' key

    Returns:
        List of parsed items.
    """
    for item in items:
        # Replace placeholder
        item["payload"] = _parse_placeholder(item["payload"], placeholders)

        # Compress payload
        item["payload"] = _compress(item["payload"])

        # TODO: permutate variables

        # Apply functions
        item["payload"] = _parse_functions(item["payload"])

    return items


def _parse_placeholder(data: str, placeholders: Dict[str, str]) -> str:
    """Returns data with placeholders replaced."""
    # Replace placeholder
    for key, val in placeholders.items():
        data = data.replace(key, val)
    return data


def _parse_functions(data: str) -> str:
    """Replaces <FUN:0...> to <FUN:9...> with their function outputs."""
    for num in range(0, 10):
        pattern = fr"(<FUN:{num}:(.+?)>(.+?)<\/FUN:{num}:\2>)"
        reg = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)
        ret = reg.findall(data)

        for match in ret:
            repl = match[0]  # Whole string to replace
            func = match[1]  # Function name, e.g. base64
            find = match[2]  # String in between function delimiter
            data = data.replace(repl, run(find, func))
    return data


def _compress(data: str) -> str:
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
        return _compress(temp)
    return temp
