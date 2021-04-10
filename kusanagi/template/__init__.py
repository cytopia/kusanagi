"""Template module."""

from typing import Dict, List, Any

import os
import sys
import pathlib

from .yaml_loader import YamlLoader
from .parser.placeholder import Placeholder
from .parser.permutator import Permutator
from .parser.compresser import Compresser
from .parser.function import Function
from .ds import DsPayload
from .ds import DsPayloadFilter
from ..core.encoder import encode


def load(addr: str, port: str) -> List[DsPayload]:
    """Returns a list of loaded DsPayload data types."""
    path = os.fspath(pathlib.Path(__file__).parent.absolute())
    path = os.fspath(os.path.join(path, "data"))
    path = os.fspath(os.path.join(path, "cmd-reverse-tcp-bash.yml"))

    data = YamlLoader.load(path)
    payloads = []

    for key, items in data["payloads"].items():
        for i in range(len(items["items"])):
            # Ensure __ADDR__ and __PORT__ placeholders are parsed and replaced.
            data["payloads"][key][i] = Placeholder.parse(items["items"][i], addr, port)

            # Mutate items based on defined variables and values
            for permutation in Permutator.get_item_permutations(items["items"][i]):
                # Compress codes
                permutation["payload"] = Compresser.trim(permutation["payload"])

                # Evaluate functions
                permutation["original"].append(permutation["payload"])
                permutation["payload"] = Function.eval(permutation["payload"])

                # Create filters
                filters = DsPayloadFilter(
                    key,
                    permutation["filters"]["shells"],
                    permutation["filters"]["os"],
                    permutation["filters"]["commands"],
                    permutation["filters"]["proto"],
                    permutation["filters"]["direction"],
                    permutation["filters"]["obfuscator"],
                )

                # Append to DsPayload data structure
                payloads.append(
                    DsPayload(
                        permutation["name"],
                        permutation["desc"],
                        key,
                        filters,
                        permutation["payload"],
                        permutation["original"],
                    )
                )
    return payloads
