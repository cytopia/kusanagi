"""Main file for kusanagi."""

from typing import Callable, Any

import os
import sys
import time
import timeit
import pathlib

from .args import *
from .lib.clipboard import copy_to_clipboard
from .template import *
from .output import output
from .filter import filter_os
from .filter import filter_badchars
from .filter import filter_executables
from .filter import filter_shells
from .filter import filter_maxlen
from .sorter import sort_by_length

from .core.payload.cmd import get_payloads


def main() -> None:
    """Run main entrypoint."""
    cmd_args = get_args()

    if cmd_args.payload in ["file", "code"]:
        print(f"{cmd_args.payload} method not yet implemented")
        sys.exit(0)

    # Retrieve payloads
    payloads = get_payloads(cmd_args.addr, str(cmd_args.port))

    # Filter payloads
    payloads = filter_executables(payloads, cmd_args.exe)
    payloads = filter_shells(payloads, cmd_args.shell)
    payloads = filter_os(payloads, cmd_args.os)
    payloads = filter_badchars(payloads, cmd_args.badchars)
    payloads = filter_maxlen(payloads, cmd_args.maxlen)

    # Sort payloads
    payloads = sort_by_length(payloads)

    # [OUTPUT] If no copy was specified, just output the payloads
    if cmd_args.copy == -1:
        output(payloads, cmd_args.addr, str(cmd_args.port), cmd_args.enc, cmd_args.quick)
        sys.exit(0)

    # [COPY] Copy payload to clipboard
    index = cmd_args.copy
    if cmd_args.copy is None:
        # Copy last element to clipboard
        index = -1
    try:
        copy_to_clipboard(payloads[index].payload)
    except IndexError:
        print(f"[ERROR] payload with index {index} does not exist", file=sys.stderr)
        sys.exit(1)
    else:
        payload = payloads[index]
        output([payload], cmd_args.addr, str(cmd_args.port), cmd_args.enc, True)
        print("copied", file=sys.stderr)


if __name__ == "__main__":
    main()
