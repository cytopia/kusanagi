"""Output module."""

from typing import List, Dict, Optional, Any
import sys
import re
from .printer import Printer
from .clipboard import copy_to_clipboard
from .encoder import encode


def output_payloads(
    items: List[Dict[str, Any]],
    payload: Dict[str, Any],
    encoders: List[str],
    options: Dict[str, Any],
) -> None:
    """Output/print payloads to terminal.

    Args:
        items (List[dict]): The payload items to print
        payload (dict): Payload type information.
        encoders (List[str]): Output encoder.
        options (dict): Copy to clipboard/show details
    """
    p = Printer(True)

    # Copy payload to clipboard
    if options["copy"] != -1:
        copy_item(p, items, options["copy"], encoders)
        return None

    # Show info output
    # if options["info"] != -1:
    #     print("TODO: INFO")
    #     return None

    # Show quick output
    if options["quick"]:
        for i, _ in enumerate(items):
            output_header_small(p, items[i], i)
            output_payload(p, items[i], encoders)
        return None

    # Show normal (verbose output)
    for i, _ in enumerate(items):
        output_header_big(p, items[i], i)
        output_revshell_info(p, items[i], payload)
        output_target_requirements(p, items[i], payload)
        output_inject_requirements(p, items[i])
        output_build_requirements(p, items[i])
        output_help(p, i)
        output_encoders(p, items[i], encoders)
        output_payload(p, items[i], encoders)
    return None


def copy_item(
    p: Printer, items: List[Dict[str, Any]], index: Optional[int], encoders: List[str]
) -> None:
    """Copy specified item payload to clipboard."""
    # If index is none (no number specified), we will just copy the last item element
    if index is None:
        index = -1
    # Get item by index
    try:
        item = items[index]
    except IndexError:
        print(f"[ERROR] payload with index {index} does not exist", file=sys.stderr)
        sys.exit(1)
    else:
        # Encode items
        data = item["payload"]
        for encoder in encoders:
            data = encode(data, encoder)
    # Copy to clipboard
    try:
        copy_to_clipboard(data)
    except OSError as error:
        print(f"[ERROR] No clipboard mechanism available on your system\n{error}", file=sys.stderr)
        sys.exit(1)
    else:
        # Normalize item index for output
        if index == -1:
            index = len(items) - 1
        output_header_small(p, item, index)
        output_payload(p, item, encoders)
        print("copied", file=sys.stderr)


def output_header_small(p: Printer, item: Dict[str, Any], index: int) -> None:
    """Output/print item header to terminal."""
    p.stderr("")
    p.stderr("[", end="")
    p.stderr(f"{index}", "blue", end="")
    p.stderr("] ", end="")
    p.stderr(f"{item['name']}")


def output_header_big(p: Printer, item: Dict[str, Any], index: int) -> None:
    """Output payload header."""
    # Print headline
    p.stderr("")
    p.stderr("-" * 80)
    p.stderr("[", end="")
    p.stderr(f"{index}", "blue", end="")
    p.stderr("] ", end="")
    p.stderr(f"{item['name']}", "yellow")
    p.stderr("-" * 80)

    # description/info
    p.stderr(f"{item['desc']}", "yellow")
    for info in item["info"]:
        p.stderr(f"info: {info}")


def output_revshell_info(p: Printer, item: Dict[str, Any], payload: Dict[str, Any]) -> None:
    """Output payload section."""
    # Print headline
    p.stderr("")
    p.stderr("PAYLOAD", "magenta")

    # target
    p.stderr("  target:     ", end="")
    p.stderr(f"{payload['revshell']['addr']}", "blue", end="")
    p.stderr(":", end="")
    p.stderr(f"{payload['revshell']['port']}", "blue")

    # payload
    p.stderr("  type:       ", end="")
    p.stderr(payload["type"], "blue", end="")
    p.stderr(" (", end="")
    p.stderr(item["revshell"]["proto"], "blue", end="")
    p.stderr(")")

    # exe
    if "executable" in item[payload["payload"]]:
        p.stderr("  executable: ", end="")
        p.stderr(item["cmd"]["executable"], "blue")

    # language
    if "language" in item[payload["payload"]]:
        p.stderr("  language:   ", end="")
        p.stderr(item["code"]["language"], "blue", end="")
        total = len(item["code"]["requires"]["version"])
        if not total:
            p.stderr("")
        else:
            p.stderr(" (", end="")
            for i in range(total):
                p.stderr(item["code"]["requires"]["version"][i], "blue", end="")
                if i < total - 1:
                    p.stderr(", ", end="")
                else:
                    p.stderr(")")

    # obfuscated
    p.stderr("  obfuscated: ", end="")
    p.stderr(item[payload["payload"]]["obfuscated"], "blue")

    # shell
    if item["revshell"]["shell"] is not None and item["revshell"]["command"] is not None:
        p.stderr("  shell:      ", end="")
        p.stderr(item["revshell"]["shell"], "blue", end="")
        p.stderr(" (", end="")
        p.stderr(item["revshell"]["command"], end="")
        p.stderr(")")
    else:
        p.stderr("  shell:      ", end="")
        p.stderr(str(item["revshell"]["shell"]), "blue")


def output_target_requirements(p: Printer, item: Dict[str, Any], payload: Dict[str, Any]) -> None:
    """Output payload target."""
    p.stderr("")
    p.stderr("TARGET REQUIREMENTS", "magenta")

    # OS
    p.stderr("  OS:         ", end="")
    total = len(item[payload["payload"]]["requires"]["os"])
    if not total:
        p.stderr("")
    for i in range(total):
        p.stderr(item[payload["payload"]]["requires"]["os"][i], "blue", end="")
        if i < total - 1:
            p.stderr(", ", end="")
        else:
            p.stderr("")

    # commands
    p.stderr("  Commands:   ", end="")
    total = len(item[payload["payload"]]["requires"]["commands"])
    if not total:
        p.stderr("")
    for i in range(total):
        p.stderr(item[payload["payload"]]["requires"]["commands"][i], "blue", end="")
        if i < total - 1:
            p.stderr(", ", end="")
        else:
            p.stderr("")

    # functions
    if "functions" in item[payload["payload"]]["requires"]:
        p.stderr("  Functions:  ", end="")
        total = len(item["code"]["requires"]["functions"])
        if not total:
            p.stderr("")
        for i in range(total):
            p.stderr(item["code"]["requires"]["functions"][i], "blue", end="")
            if i < total - 1:
                p.stderr(", ", end="")
            else:
                p.stderr("")

    # modules
    if "modules" in item[payload["payload"]]["requires"]:
        p.stderr("  Modules:    ", end="")
        total = len(item["code"]["requires"]["modules"])
        if not total:
            p.stderr("")
        for i in range(total):
            p.stderr(item["code"]["requires"]["modules"][i], "blue", end="")
            if i < total - 1:
                p.stderr(", ", end="")
            else:
                p.stderr("")

    # shell_env
    if "shell_env" in item[payload["payload"]]["requires"]:
        p.stderr("  Shell envs: ", end="")
        total = len(item[payload["payload"]]["requires"]["shell_env"])
        if not total:
            p.stderr("")
        for i in range(total):
            p.stderr(item[payload["payload"]]["requires"]["shell_env"][i], "blue", end="")
            if i < total - 1:
                p.stderr(", ", end="")
            else:
                p.stderr("")


def output_inject_requirements(p: Printer, item: Dict[str, Any]) -> None:
    """Output payload target."""
    p.stderr("")
    p.stderr("INJECT REQUIREMENTS", "magenta")

    # bytes
    p.stderr("  size:       ", end="")
    p.stderr(str(len(item["payload"])), "blue", end="")
    p.stderr(" bytes")

    # badchars
    p.stderr("  badchars:   ", end="")
    p.stderr(_get_badchars(item["payload"]), "blue")


def output_build_requirements(p: Printer, item: Dict[str, Any]) -> None:
    """Output how the payload has been assembled."""
    if not item["builder"]:
        return

    p.stderr("")
    p.stderr("ASSEMBLING", "magenta")
    for i, step in enumerate(item["builder"]):
        p.stderr(f"  {i+1}. ", end="")
        p.stderr(step, "blue")


def output_help(p: Printer, index: int) -> None:
    """Output payload target."""
    p.stderr("")
    p.stderr("# Append '", "green", end="")
    p.stderr(f"-c {index}", "blue", end="")
    p.stderr("' to copy payload to clipboard", "green")

    p.stderr("# Append '", "green", end="")
    p.stderr(f"-q {index}", "blue", end="")
    p.stderr("' to display payload details", "green")
    p.stderr("")


def output_encoders(p: Printer, item: Dict[str, Any], encoders: List[str]) -> None:
    """Output final payload."""
    data = item["payload"]

    # Apply output encoders
    for encoder in encoders:
        data = encode(data, encoder)

    # output encoder
    total = len(encoders)
    if total:
        # encoders used
        p.stderr("output encoder:   ", end="")
        for i in range(total):
            p.stderr(f"{encoders[i]}", "green", end="")
            if i < total - 1:
                p.stderr(" -> ", end="")
            else:
                p.stderr("")
        # encoded size
        p.stderr("encoded size:     ", end="")
        p.stderr(str(len(data)), "green", end="")
        p.stderr(" bytes")
        # encoded badchars
        p.stderr("encoded badchars: ", end="")
        p.stderr(_get_badchars(data), "green")
        p.stderr("")


def output_payload(p: Printer, item: Dict[str, Any], encoders: List[str]) -> None:
    """Output final payload."""
    data = item["payload"]

    # Apply output encoders
    for encoder in encoders:
        data = encode(data, encoder)
    p.stdout(data, "yellow")
    p.stderr("")


def _get_badchars(data: str) -> str:
    """Returns the badchars contained in a string."""
    regex = r"[^a-zA-Z0-9\s]"
    match = re.findall(regex, data)
    match = sorted(set(match))  # unique and sort
    return "".join(match)
