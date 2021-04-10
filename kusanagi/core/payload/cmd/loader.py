"""This file provides functions to load the obfuscators."""

from typing import List, Dict, Any

import os
import pathlib

from .validator import VALIDATOR
from ...permutator import permutate_variables
from ...permutator import obfuscate_payloads
from ...obfuscator import get_obfuscators
from ...typing.ds_payload import DsPayload
from ...typing.ds_payload_filter import DsPayloadFilter
from ....lib.yaml import load as load_yaml
from ....lib.template import get_template_dir
from ...parser import parse_functions
from ...compressor import compress


# Available obfuscator files
PAYLOADS = [
    "bash.yml",
    "nc.yml",
]


def _load(placeholders: Dict[str, str]) -> List[DsPayload]:
    """Load available payloads."""
    payloads = []
    obfuscators = get_obfuscators()

    for name in PAYLOADS:
        # Load payload file
        path = get_template_dir(["payloads", "cmd", name])
        data = load_yaml(path, VALIDATOR)

        for item in data["payloads"]:
            # Replace placeholder
            for key, val in placeholders.items():
                item["payload"] = item["payload"].replace(key, val)

            # Update the cmd filter accordingly
            item["filters"]["cmd"] = data["command"]

            # Compress payload
            item["payload"] = compress(item["payload"])

            # Parse functions
            item["payload"] = parse_functions(item["payload"])

            # Permutate variables
            for payload in permutate_variables(item):

                # Append de-variablized payload to list
                payloads.append(_get_payload_from_item(payload))

                # Permutate obfuscations
                for obfuscated in obfuscate_payloads(payload, obfuscators):
                    # TODO: Do I have to add it back to "original" before?

                    # Compress payload
                    obfuscated["payload"] = compress(obfuscated["payload"])

                    # Parse function
                    obfuscated["payload"] = parse_functions(obfuscated["payload"])
                    # Append obfuscated payload to list
                    payloads.append(_get_payload_from_item(obfuscated))
    return payloads


def _get_payload_from_item(item: Dict[str, List]) -> DsPayload:
    """Returns DsPayload data structure from item."""
    filters = DsPayloadFilter(
        item["filters"]["cmd"],
        item["filters"]["cmd_exe"],
        item["filters"]["shell"],
        item["filters"]["cmd_shell"],
        item["filters"]["shells"],
        item["filters"]["os"],
        item["filters"]["commands"],
        item["filters"]["proto"],
        item["filters"]["direction"],
        item["filters"]["encoders"],
    )
    # Return Payload
    return DsPayload(
        item["name"],
        item["desc"],
        item["info"],
        item["filters"]["cmd"],
        item["meta"],
        filters,
        item["payload"],
        item["original"],
    )
