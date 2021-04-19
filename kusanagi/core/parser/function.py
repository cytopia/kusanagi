"""Provides template functions."""

import base64
import re
import html
import urllib.parse


# --------------------------------------------------------------------------------------------------
# Public functions
# --------------------------------------------------------------------------------------------------
def run(data: str, function_name: str) -> str:
    """Runs a function on data and returns function output.

    Args:
        data (str): The string to run the function against.
        function_name (str): The function to run.

    Returns:
        str: Result of the function applied on data.
    """
    func = globals()["_get_" + function_name]
    data = func(data)
    return data


# --------------------------------------------------------------------------------------------------
# Available Template Functions
# --------------------------------------------------------------------------------------------------
def _get_len(data: str) -> str:
    """Returns the length of data."""
    return str(len(data))


def _get_url(data: str) -> str:
    """URL encodes data."""
    return urllib.parse.quote(data, safe="")


def _get_urlplus(data: str) -> str:
    """URL encodes data and converts spaces to a '+' sign."""
    return urllib.parse.quote_plus(data, safe="")


def _get_html(data: str) -> str:
    """Html entity encodes data."""
    return html.escape(data)


def _get_hex(data: str) -> str:
    r"""Returns '\xff' hex representation of data."""
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", "\\x"))
    return "".join(temp)


def _get_hexesc(data: str) -> str:
    r"""Returns '\\xff' escaped-hex representation of data."""
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", "\\\\x"))
    return "".join(temp)


def _get_hex0x(data: str) -> str:
    r"""Returns '0xff' 0-prefixed hex representation of data."""
    temp = []
    for char in data:
        temp.append(hex(ord(char)))
    return "".join(temp)


def _get_hexplain(data: str) -> str:
    """Returns hex values of data without any prefixes."""
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", ""))
    return "".join(temp)


def _get_base64(data: str) -> str:
    """Base 64 encodes data."""
    ebytes = base64.b64encode(data.encode("utf-8"))
    estring = str(ebytes, "utf-8")
    return estring


def _get_base64pad(data: str) -> str:
    """Base64 encodes with space padding to ensure output only contains [a-zA-Z0-9+]."""
    pattern = r"[^a-zA-Z0-9\+]"
    regex = re.compile(pattern)
    while True:
        ebytes = base64.b64encode(data.encode("utf-8"))
        estring = str(ebytes, "utf-8")
        if not regex.findall(estring):
            break
        # Pad with trailing space and try again to eliminate base64 pad chars
        data = data + " "

    return estring


def _get_2xbase64pad(data: str) -> str:
    """Base64 encodes twice with space padding to ensure output only contains [a-zA-Z0-9]."""
    pattern = r"[^a-zA-Z0-9]"
    regex = re.compile(pattern)
    while True:
        # First run
        ebytes = base64.b64encode(data.encode("utf-8"))
        estring = str(ebytes, "utf-8")

        # Second run
        ebytes = base64.b64encode(estring.encode("utf-8"))
        estring = str(ebytes, "utf-8")

        if not regex.findall(estring):
            break
        # Pad with trailing space and try again to eliminate base64 pad/special chars
        data = data + " "

    return estring
