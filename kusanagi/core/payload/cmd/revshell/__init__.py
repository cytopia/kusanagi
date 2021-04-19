"""Module to load reverse shell payloads."""

from typing import List, Dict, Any
from ....helper import intersect
from ....helper import unique
from ....loader import load
from ....parser import parse
from ..obfuscator import *
from .validator import VALIDATOR


CMD_FILES = [
    "bash.yml",
]

CMD_SUBDIRS = ["cmd", "revshells"]


def get_revshells(addr: str, port: str, obfuscated: bool) -> List[Dict[str, Any]]:
    """Returns list of reverse shell payloads."""
    # Final items
    items = []

    placeholders = {
        "__ADDR__": addr,
        "__PORT__": port,
    }

    # Get parsed items
    cmds = load(CMD_FILES, CMD_SUBDIRS, VALIDATOR)
    cmds = parse(cmds, placeholders)

    # Loop over items
    for cmd in cmds:

        # Add normal cmd item
        items.append(_get_revshell_item(cmd, False))

        # Add obfuscated items as well?
        if obfuscated:
            for obfuscator in get_obfuscators():
                # # Check for same language (cmd <-> obfuscator)
                # if cmd["cmd"]["language"] == obfuscator["cmd"]["language"]:
                #     # Check language version compatibility
                #     # Only obfuscate if versions (e.g. Python3 and Python3) are compatible
                #     # Also obfuscate if both have no version specified.
                #     cmd_v = cmd["cmd"]["requires"]["version"]
                #     obfu_v = obfuscator["cmd"]["requires"]["version"]
                #     if intersect(cmd_v, obfu_v) or (not cmd_v and not obfu_v):
                #         # Create obfuscated item
                #         temp = parse([obfuscator], {"__CMD__": cmd["payload"]})[0]
                #         # Append obfuscated item
                #         items.append(_get_obfuscator_item(cmd, temp))
                # Create obfuscated item
                temp = parse([obfuscator], {"__CMD__": cmd["payload"]})[0]
                # Append obfuscated item
                items.append(_get_obfuscator_item(cmd, temp))
    return items


def _get_revshell_item(cmd: Dict[str, Any], obfuscated: bool) -> Dict[str, Any]:
    """Get an item."""
    data = {
        "name": cmd["name"],
        "desc": cmd["desc"],
        "info": cmd["info"],
        "rating": cmd["rating"],
        "cmd": {
            "obfuscated": obfuscated,
            "executable": cmd["cmd"]["executable"],
            "requires": {
                "commands": cmd["cmd"]["requires"]["commands"],
                "shell_env": cmd["cmd"]["requires"]["shell_env"],
                "os": cmd["cmd"]["requires"]["os"],
            },
        },
        "revshell": {
            "proto": cmd["revshell"]["proto"],
            "shell": cmd["revshell"]["shell"],
            "command": cmd["revshell"]["command"],
        },
        "payload": cmd["payload"],
    }
    return data


def _get_obfuscator_item(cmd: Dict[str, Any], obfuscator: Dict[str, Any]) -> Dict[str, Any]:
    """Create cmd item from obfuscator."""
    data = copy.deepcopy(cmd)

    # Data is combined
    data["name"] = obfuscator["name"] + " [ " + cmd["name"] + " ]"
    data["desc"] = cmd["desc"] + " -> " + obfuscator["desc"]
    data["info"] = cmd["info"] + obfuscator["info"]

    # Commands are joined and ensured they are unique
    data["cmd"]["requires"]["commands"] += obfuscator["cmd"]["requires"]["commands"]
    data["cmd"]["requires"]["commands"] = unique(data["cmd"]["requires"]["commands"])

    # shell_env and os are intersected
    env = intersect(cmd["cmd"]["requires"]["shell_env"], obfuscator["cmd"]["requires"]["shell_env"])
    os = intersect(cmd["cmd"]["requires"]["os"], obfuscator["cmd"]["requires"]["os"])
    data["cmd"]["requires"]["shell_env"] = env
    data["cmd"]["requires"]["os"] = os

    # Evaluate overwrites
    if "overwrites" in obfuscator["cmd"]:
        if "shell_env" in obfuscator["cmd"]["overwrites"]:
            data["cmd"]["requires"]["shell_env"] = obfuscator["cmd"]["overwrites"]["shell_env"]

    data["payload"] = obfuscator["payload"]

    return _get_revshell_item(data, True)
