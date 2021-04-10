"""Module to filter payloads on their given options."""

from typing import List
from ..typing.ds_payload import DsPayload


def filter_executables(payloads: List[DsPayload], executables: List[str]) -> List[DsPayload]:
    """Returns only payloads for given list of executables."""
    if not executables:
        return payloads

    filtered = []
    for payload in payloads:
        if payload.filters.exe in executables:
            filtered.append(payload)
    return filtered


def filter_shells(payloads: List[DsPayload], shells: List[str]) -> List[DsPayload]:
    """Returns only payloads which work when executed on specific underlying shells."""
    if not shells:
        return payloads

    filtered = []
    for payload in payloads:
        has_shell = False
        for shell in shells:
            if shell in payload.filters.shells:
                has_shell = True
        if has_shell:
            filtered.append(payload)
    return filtered


def filter_os(payloads: List[DsPayload], os: str) -> List[DsPayload]:
    """Returns only payloads for a given os."""
    if not os:
        return payloads

    filtered = []
    for payload in payloads:
        if os in payload.filters.os:
            filtered.append(payload)
    return filtered


def filter_badchars(payloads: List[DsPayload], badchars: str) -> List[DsPayload]:
    """Returns only payloads without specified badcharss."""
    if not badchars:
        return payloads

    filtered = []
    for payload in payloads:
        has_badchar = False
        for badchar in badchars:
            if badchar in payload.payload:
                has_badchar = True
        if not has_badchar:
            filtered.append(payload)
    return filtered


def filter_maxlen(payloads: List[DsPayload], maxlen: int) -> List[DsPayload]:
    """Returns only payloads not longer than maxlen."""
    if maxlen <= 0:
        return payloads

    filtered = []
    for payload in payloads:
        if len(payload.payload) <= maxlen:
            filtered.append(payload)
    return filtered
