"""Encoder module."""
from typing import Dict, List, Any
from argparse import ArgumentTypeError

import os
import pathlib
import base64
import re
import html
import urllib.parse


AVAILABLE_ENCODERS = {
    "url": "URL encodes the data.",
    "urlplus": "URL encodes the data and converts spaces to '+' signs",
    "html": "Convert all applicable characters to HTML entities",
    "hex": "Convert to hex, prepended with \\x",
    "hexesc": "Convert to hex, prepended with escaped \\\\x (double slash)",
    "hex0x": "Convert to hex, prepended with 0x",
    "hexplain": "Convert to hex characters, no prefix",
    "base64": "base64 encoding",
    "base64pad": "base64 encoding with padding to achieve: [A-Za-z0-9+]",
    "2xbase64pad": "Double base64 encoding with padding to achieve: [A-Za-z0-9]",
}


# --------------------------------------------------------------------------------------------------
# Public functions
# --------------------------------------------------------------------------------------------------
def encode(data: str, encoder_name: str) -> str:
    """Encodes a string with the given encoder name."""
    func = globals()["_encode_" + encoder_name]
    data = func(data)
    return data


# --------------------------------------------------------------------------------------------------
# Public argparse functions
# --------------------------------------------------------------------------------------------------
def argparse_encoder_validate(encoder: str) -> str:
    """Argparse choice function to select encoders."""
    if encoder not in AVAILABLE_ENCODERS:
        raise ArgumentTypeError("%s is an invalid encoder." % encoder)
    return encoder


def argparse_encoder_list() -> None:
    """List available encoder for argument --list-encoders."""
    print("Available encoders:\n")
    print("{:<12}| {}".format("NAME", "DESCRIPTION"))
    print("{}|{}".format("-" * 12, "-" * 12))
    for encoder in AVAILABLE_ENCODERS:
        print("{:<12}| {}".format(encoder, AVAILABLE_ENCODERS[encoder]))


# --------------------------------------------------------------------------------------------------
# Available Encoders
# --------------------------------------------------------------------------------------------------


def _encode_url(data: str) -> str:
    """URL encodes the string."""
    return urllib.parse.quote(data, safe="")


def _encode_urlplus(data: str) -> str:
    """URL encodes the string and converts spaces to a '+' sign."""
    return urllib.parse.quote_plus(data, safe="")


def _encode_html(data: str) -> str:
    """Html entity encodes the string."""
    return html.escape(data)


def _encode_hex(data: str) -> str:
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", "\\x"))
    return "".join(temp)


def _encode_hexesc(data: str) -> str:
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", "\\\\x"))
    return "".join(temp)


def _encode_hex0x(data: str) -> str:
    temp = []
    for char in data:
        temp.append(hex(ord(char)))
    return "".join(temp)


def _encode_hexplain(data: str) -> str:
    temp = []
    for char in data:
        temp.append(hex(ord(char)).replace("0x", ""))
    return "".join(temp)


def _encode_base64(data: str) -> str:
    """Base 64 encodes a string."""
    ebytes = base64.b64encode(data.encode("utf-8"))
    estring = str(ebytes, "utf-8")
    return estring


def _encode_base64pad(data: str) -> str:
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


def _encode_2xbase64pad(data: str) -> str:
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
