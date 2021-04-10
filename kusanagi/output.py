"""Module to output the payloads on the command line."""

from typing import List, Optional, Any
import sys
import re

from termcolor import cprint

from .core.typing.ds_payload import DsPayload
from .core.encoder import encode


# --------------------------------------------------------------------------------------------------
# Public module functions
# --------------------------------------------------------------------------------------------------
def output(
    payloads: List[DsPayload], addr: str, port: str, encoders: List[str], quick: bool
) -> None:
    """Output payloads based on users choice."""
    if quick:
        for i, _ in enumerate(payloads):
            _print_payload(payloads[i], encoders, i)
    else:
        for i, _ in enumerate(payloads):
            _print_payload_verbose(payloads[i], addr, port, encoders, i)


# --------------------------------------------------------------------------------------------------
# Private module functions
# --------------------------------------------------------------------------------------------------
class Out:
    """stdout, stderr print class with color support."""

    def __init__(self, colored: bool) -> None:
        self.__colored = colored

    def stderr(self, text: str, color: Optional[str] = None, **kwargs: Any) -> None:
        """Print to stderr with or without color depending on instance settings."""
        if self.__colored:
            cprint(text, color, file=sys.stderr, **kwargs)
        else:
            print(text, file=sys.stderr, **kwargs)

    def stdout(self, text: str, color: Optional[str] = None, **kwargs: Any) -> None:
        """Print to stdout with or without color depending on instance settings."""
        if self.__colored:
            cprint(text, color, **kwargs)
        else:
            print(text, **kwargs)


def _print_payload(
    payload: DsPayload,
    encoders: List[str],
    index: int,
) -> None:
    """Print a single payload with less verbosity."""
    data = payload.payload

    # Apply output encoders
    for encoder in encoders:
        data = encode(data, encoder)

    p = Out(True)

    # Print headline
    p.stderr("")
    p.stderr("[", end="")
    p.stderr(f"{index}", "blue", end="")
    p.stderr("] ", end="")
    p.stderr(f"{payload.name}")
    # Print payload
    p.stdout(data, "red")


def _print_payload_verbose(
    payload: DsPayload,
    addr: str,
    port: str,
    encoders: List[str],
    index: int,
) -> None:
    """Print a single payload with more verbosity."""
    data = payload.payload

    # Apply output encoders
    for encoder in encoders:
        data = encode(data, encoder)

    p = Out(True)

    # Print headline
    p.stderr("")
    p.stderr("-" * 80)
    p.stderr("[", end="")
    p.stderr(f"{index}", "blue", end="")
    p.stderr("] ", end="")
    p.stderr(f"{payload.name}", "yellow")
    p.stderr("-" * 80)

    # description/info
    p.stderr(f"{payload.desc}", "yellow")
    for info in payload.info:
        p.stderr(f"info: {info}")

    # ------------------------------------------------------------
    # Payload
    # ------------------------------------------------------------
    p.stderr("")
    p.stderr("PAYLOAD", "magenta")

    # target
    p.stderr("  target:     ", end="")
    p.stderr(f"{addr}", "blue", end="")
    p.stderr(":", end="")
    p.stderr(f"{port}", "blue")

    # exe
    p.stderr("  executable  ", end="")
    p.stderr(payload.filters.exe, "blue", end="")
    p.stderr(" (", end="")
    p.stderr(f"{payload.filters.cmd_exe}", end="")
    p.stderr(")")

    # shell
    p.stderr("  shell       ", end="")
    p.stderr(payload.filters.shell, "blue", end="")
    p.stderr(" (", end="")
    p.stderr(f"{payload.filters.cmd_shell}", end="")
    p.stderr(")")

    # proto
    p.stderr("  protocol:   ", end="")
    p.stderr(f"{payload.filters.proto}", "blue")

    # direction
    p.stderr("  direction:  ", end="")
    p.stderr(f"{payload.filters.direction}", "blue")

    # ------------------------------------------------------------
    # Target Requirements
    # ------------------------------------------------------------
    p.stderr("")
    p.stderr("TARGET REQUIREMENTS", "magenta")

    # OS
    p.stderr("  OS:         ", end="")
    total = len(payload.filters.os)
    if not total:
        p.stderr("")
    for i in range(total):
        p.stderr(f"{payload.filters.os[i]}", "blue", end="")
        if i < total - 1:
            p.stderr(", ", end="")
        else:
            p.stderr("")

    # Underlying shells
    p.stderr("  Works from: ", end="")
    total = len(payload.filters.shells)
    if not total:
        p.stderr("")
    for i in range(total):
        p.stderr(f"{payload.filters.shells[i]}", "blue", end="")
        if i < total - 1:
            p.stderr(", ", end="")
        else:
            p.stderr("")

    # commands
    p.stderr("  Commands:   ", end="")
    total = len(payload.filters.commands)
    if not total:
        p.stderr("")
    for i in range(total):
        p.stderr(f"{payload.filters.commands[i]}", "blue", end="")
        if i < total - 1:
            p.stderr(" and ", end="")
        else:
            p.stderr("")

    # ------------------------------------------------------------
    # Inject Requirements
    # ------------------------------------------------------------
    p.stderr("")
    p.stderr("INJECT REQUIREMENTS", "magenta")

    # bytes
    p.stderr("  size:       ", end="")
    p.stderr(str(len(payload.payload)), "blue", end="")
    p.stderr(" bytes")

    # badchars
    p.stderr("  badchars:   ", end="")
    p.stderr(_get_badchars(payload.payload), "blue")

    # # obfuscator
    # p.stderr("encoders: ", end="")
    # total = len(payload.filters.encoders)
    # if not total:
    #     p.stderr("")
    # for i in range(total):
    #     p.stderr(f"{payload.filters.encoders[i]}", "blue", end="")
    #     if i < total-1:
    #         p.stderr(", ", end="")
    #     else:
    #         p.stderr("")

    # HELP
    p.stderr("")
    p.stderr("# Use '", "green", end="")
    p.stderr(f"-c {index}", "blue", end="")
    p.stderr("' to copy payload to clipboard", "green")

    p.stderr("# Use '", "green", end="")
    p.stderr(f"-q {index}", "blue", end="")
    p.stderr("' to display payload details", "green")

    # output encoder
    total = len(encoders)
    if total:
        p.stderr("")
        p.stderr("output encoder: ", end="")
        for i in range(total):
            p.stderr(f"{encoders[i]}", "green", end="")
            if i < total - 1:
                p.stderr(" -> ", end="")
            else:
                p.stderr("")
        # encoded size
        p.stderr("encoded size:   ", end="")
        p.stderr(str(len(data)), "green", end="")
        p.stderr(" bytes")

    p.stderr("")
    p.stdout(data, "red")
    p.stderr("")


def _get_badchars(data: str) -> str:
    """Returns the badchars contained in a string."""
    regex = r"[^a-zA-Z0-9\s]"
    match = re.findall(regex, data)
    match = sorted(set(match))  # unique and sort
    return "".join(match)
