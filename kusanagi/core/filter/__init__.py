"""Module to filter payloads on their given options."""

from typing import List, Dict, Any


def filter_executables(items: List[Dict[str, Any]], executables: List[str]) -> List[Dict[str, Any]]:
    """Returns only payloads for given list of executables."""
    if not executables:
        return items

    filtered = []
    for item in items:
        if item["cmd"]["executable"] in executables:
            filtered.append(item)
    return filtered


def filter_languages(items: List[Dict[str, Any]], languages: List[str]) -> List[Dict[str, Any]]:
    """Returns only payloads for given list of languages."""
    if not languages:
        return items

    filtered = []
    for item in items:
        if "code" in item:
            if item["code"]["language"] in languages:
                filtered.append(item)
    return filtered


def filter_shells(items: List[Dict[str, Any]], shells: List[str]) -> List[Dict[str, Any]]:
    """Returns only payloads which work when executed on specific underlying shells."""
    if not shells:
        return items

    filtered = []
    for item in items:
        has_shell = False
        for shell in shells:
            if "revshell" in item and shell in item["revshell"]["shell"]:
                has_shell = True
            if "bindshell" in item and shell in item["bindshell"]["shell"]:
                has_shell = True
        if has_shell:
            filtered.append(item)
    return filtered


def filter_os(items: List[Dict[str, Any]], os: str) -> List[Dict[str, Any]]:
    """Returns only payloads for a given os."""
    if not os:
        return items

    filtered = []
    for item in items:
        if "cmd" in item and os in item["cmd"]["requires"]["os"]:
            filtered.append(item)
        if "code" in item and os in item["code"]["requires"]["os"]:
            filtered.append(item)
        if "file" in item and os in item["file"]["requires"]["os"]:
            filtered.append(item)
    return filtered


def filter_badchars(items: List[Dict[str, Any]], badchars: str) -> List[Dict[str, Any]]:
    """Returns only payloads without specified badcharss."""
    if not badchars:
        return items

    filtered = []
    for item in items:
        has_badchar = False
        for badchar in badchars:
            if badchar in item["payload"]:
                has_badchar = True
        if not has_badchar:
            filtered.append(item)
    return filtered


def filter_maxlen(items: List[Dict[str, Any]], maxlen: int) -> List[Dict[str, Any]]:
    """Returns only payloads not longer than maxlen."""
    if maxlen <= 0:
        return items

    filtered = []
    for item in items:
        if len(item["payload"]) <= maxlen:
            filtered.append(item)
    return filtered
