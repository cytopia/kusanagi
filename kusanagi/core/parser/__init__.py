"""This module will evaluate defined functions."""

import re
from ..encoder import encode


def parse_functions(data: str) -> str:
    """Replaces <FUN:0...> to <FUN:9...> with their function outputs."""
    for num in range(0, 10):
        pattern = fr"(<FUN:{num}:(.+?)>(.+?)<\/FUN:{num}:\2>)"
        reg = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)
        ret = reg.findall(data)

        for match in ret:
            repl = match[0]  # Whole string to replace
            func = match[1]  # Function name, e.g. base64
            find = match[2]  # String in between function delimiter
            data = data.replace(repl, encode(find, func))
    return data
