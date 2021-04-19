"""Main file for kusanagi."""

from typing import Callable, Any

import sys

from .args import *

from .core.output import output_payloads
from .core.payload import filter_items
from .core.payload import sort_items

from .core.payload import code
from .core.payload import cmd


def main() -> None:
    """Run main entrypoint."""
    cmd_args = get_args()

    print(cmd_args)

    output_options = {
        "quick": cmd_args.quick,
        "copy": cmd_args.copy,
        "info": None,
    }

    # TODO: Make this an option via command line to select bind-/reverse shell
    payload = {
        "payload": cmd_args.payload,
        "type": "revshell",
        "revshell": {
            "addr": cmd_args.addr,
            "port": str(cmd_args.port),
        },
    }

    # Output code
    if cmd_args.payload == "code":
        filters = {
            "lang": cmd_args.lang,
            "shells": cmd_args.shell,
            "os": cmd_args.os,
            "badchars": cmd_args.badchars,
            "maxlen": cmd_args.maxlen,
            "obfuscate": cmd_args.obf,
        }

        items = code.get_items(
            "revshell",
            cmd_args.obf,
            {
                "addr": cmd_args.addr,
                "port": str(cmd_args.port),
            },
        )
        items = filter_items(items, filters)
        items = sort_items(items, "default")
        output_payloads(items, payload, cmd_args.enc, output_options)

    # Output commands
    if cmd_args.payload == "cmd":
        filters = {
            "exe": cmd_args.exe,
            "shells": cmd_args.shell,
            "os": cmd_args.os,
            "badchars": cmd_args.badchars,
            "maxlen": cmd_args.maxlen,
            "obfuscate": cmd_args.obf,
        }
        items = cmd.get_items(
            "revshell",
            cmd_args.obf,
            {
                "addr": cmd_args.addr,
                "port": str(cmd_args.port),
            },
        )
        items = filter_items(items, filters)
        items = sort_items(items, "default")
        output_payloads(items, payload, cmd_args.enc, output_options)


if __name__ == "__main__":
    main()
