"""Code Module."""
from typing import List, Dict, Any

from .revshell import get_revshells


def get_items(payload: str, obfuscated: bool, options: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Returns list of payload items by 'payload' type with corresponding payload options.

    Args:
        payload (str): Payload type (revshell, bindshell)
        options (dict): Payload options for the corresponding type.

    Returns:
        List[dict]: List of payload items.
    """
    if payload == "revshell":
        return get_revshells(options["addr"], options["port"], obfuscated)
    return []
