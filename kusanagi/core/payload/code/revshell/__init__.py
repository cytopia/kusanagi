"""Module to load reverse shell payloads."""

from typing import List, Dict, Any
from ....helper import intersect
from ....helper import unique
from ....loader import load
from ....parser import parse
from ..obfuscator import *
from .validator import VALIDATOR


CODE_FILES = [
    "bash.yml",
    "php.yml",
    "python.yml",
    "ruby.yml",
]

CODE_SUBDIRS = ["code", "revshells"]


def get_revshells(addr: str, port: str, obfuscated: bool) -> List[Dict[str, Any]]:
    """Returns list of reverse shell payloads."""
    # Final items
    items = []

    placeholders = {
        "__ADDR__": addr,
        "__PORT__": port,
    }

    # Get parsed items
    codes = load(CODE_FILES, CODE_SUBDIRS, VALIDATOR)
    codes = parse(codes, placeholders)

    # Loop over items
    for code in codes:

        # Add normal code item
        items.append(_get_revshell_item(code, False))

        # Add obfuscated items as well?
        if obfuscated:
            for obfuscator in get_obfuscators():
                # Check for same language (code <-> obfuscator)
                if code["code"]["language"] == obfuscator["code"]["language"]:
                    # Check language version compatibility
                    # Only obfuscate if versions (e.g. Python3 and Python3) are compatible
                    # Also obfuscate if both have no version specified.
                    code_v = code["code"]["requires"]["version"]
                    obfu_v = obfuscator["code"]["requires"]["version"]
                    if intersect(code_v, obfu_v) or (not code_v and not obfu_v):
                        # Create obfuscated item
                        code["builder"] = [code["payload"], obfuscator["payload"]]
                        temp = parse([obfuscator], {"__CODE__": code["payload"]})[0]
                        # Append obfuscated item
                        items.append(_get_obfuscator_item(code, temp))
    return items


def _get_revshell_item(item: Dict[str, Any], obfuscated: bool) -> Dict[str, Any]:
    """Get an item."""
    builder = item["builder"] if "builder" in item else []
    data = {
        "name": item["name"],
        "desc": item["desc"],
        "info": item["info"],
        "rating": item["rating"],
        "code": {
            "obfuscated": obfuscated,
            "language": item["code"]["language"],
            "requires": {
                "version": item["code"]["requires"]["version"],
                "commands": item["code"]["requires"]["commands"],
                "functions": item["code"]["requires"]["functions"],
                "modules": item["code"]["requires"]["modules"],
                "os": item["code"]["requires"]["os"],
            },
        },
        "revshell": {
            "proto": item["revshell"]["proto"],
            "shell": item["revshell"]["shell"],
            "command": item["revshell"]["command"],
        },
        "builder": builder,
        "payload": item["payload"],
    }
    return data


def _get_obfuscator_item(code: Dict[str, Any], obfuscator: Dict[str, Any]) -> Dict[str, Any]:
    """Create code item from obfuscator."""
    data = copy.deepcopy(code)

    # Data is combined
    data["name"] = obfuscator["name"] + " [ " + code["name"] + " ]"
    data["desc"] = code["desc"] + " -> " + obfuscator["desc"]
    data["info"] = code["info"] + obfuscator["info"]

    # Merge functions and modules
    data["code"]["requires"]["functions"] += obfuscator["code"]["requires"]["functions"]
    data["code"]["requires"]["modules"] += obfuscator["code"]["requires"]["modules"]
    # Ensure lists have unique items only
    data["code"]["requires"]["functions"] = unique(data["code"]["requires"]["functions"])
    data["code"]["requires"]["modules"] = unique(data["code"]["requires"]["modules"])

    # version and os are intersected
    ver = intersect(code["code"]["requires"]["version"], obfuscator["code"]["requires"]["version"])
    os = intersect(code["code"]["requires"]["os"], obfuscator["code"]["requires"]["os"])
    data["code"]["requires"]["version"] = ver
    data["code"]["requires"]["os"] = os
    data["payload"] = obfuscator["payload"]

    return _get_revshell_item(data, True)
