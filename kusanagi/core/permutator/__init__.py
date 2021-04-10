"""Permutator Module which permutates payloads or obfuscator items.

Permutation is first done on all possible combination of defined variables and their values
on a payload or obfuscator item.
Example: If one item has two variables defined and the first one has two values and the second one
has four values, then the final variable permutation is 2*4 == 8.

Then each payload item is permutated with all available obfuscators that are working on that item.
If an obfuscator works for a payload is determined by their 'filters.shells[]' list.
If both (payload and obfuscator) have the same value in that filter, they will work.
The filters.shells list will then be intersected.
"""

from typing import Dict, List, Union, Any

import copy
import re
import itertools


def obfuscate_payloads(
    payload: Dict[str, Any],
    obfuscators: List[Dict[Any, Any]],
) -> List[Dict[Any, Any]]:
    """Create payload variations for each available obfuscator.

    This should be done after variable permutations.
    Obfuscators and payloads will be matched based on their 'filters.shells' (list).
    The created list will also intersect filters.shells and merge filters.commands and
    filters.encoders.

    Args:
        payload (Dict[str, Any]): Payload item
        obfuscators (List[Dict[Any, Any]]): all available obfuscators

    Returns:
        dict: Python dict from yaml file.
    """
    items = []
    for obfuscator in obfuscators:
        for shell in obfuscator["filters"]["shells"]:
            # We have found an obfuscator that will work for the payload
            if shell in payload["filters"]["shells"]:
                item = copy.deepcopy(payload)
                # Intersect filters.shells
                shells = list(set(item["filters"]["shells"]) & set(obfuscator["filters"]["shells"]))
                item["filters"]["shells"] = shells

                # Combine filters.commands and filters.encoders
                commands = item["filters"]["commands"] + obfuscator["filters"]["commands"]
                encoders = item["filters"]["encoders"] + obfuscator["filters"]["encoders"]
                item["filters"]["commands"] = list(set(commands))  # Ensure unique items
                item["filters"]["encoders"] = list(set(encoders))  # Ensure unique items

                # Append original string to original
                item["original"].append(item["payload"])

                # Replace payload
                item["payload"] = obfuscator["payload"].replace("__PAYLOAD__", item["payload"])

                # Append items
                items.append(item)

    return items


def permutate_variables(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Creates mutations for each available mutation variable.

    This function will make as many copies of the input item as there are
    variable combinations/permutations. It will then copy back the variables[].filters
    into top-level filters of that permutation and finally replace the variables in
    payload and top-level filters values.

    Returns:
        List[Dict[str, Any]]: List of mutated items.
    """
    # TODO/FIXME: Make this function nicer, better var naming
    items = []
    # Replace with available variables

    # If no mutation variables are defined, we just take
    # the item as it is and return it as a list item.
    if not item["variables"]:
        if "original" not in item:
            item["original"] = []
        return [item]

    # variable_dict = {
    #   '<varname>': [
    #     {'value': '<value-1>', 'filters': {}},
    #     {'value': '<value-2>', 'filters': {}},
    #   ]
    # }
    variable_dict = {var["name"]: var["values"] for var in item["variables"]}
    # Get all combinations of defined variable mutations
    # https://stackoverflow.com/a/61335465
    keys, values = zip(*variable_dict.items())

    # permutations = [
    #   {'<varname>': {'value': '<value-1>', 'filters': None}},
    #   {'<varname>': {'value': '<value-2>', 'filters': None}}
    # ]
    permutations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    # permutations = [
    #   {
    #     varX: [value: valX-1, filters: {}]
    #     varY: [value: valY-1, filters: {}]
    #   }
    #   {
    #     varX: [value: valX-2, filters: {}]
    #     varY: [value: valY-1, filters: {}]
    #   }
    # ]
    for variables in permutations:
        # <var-name> : {
        #   {varX: {value: valX-1, filters: {}},
        #   {varY: {value: valY-1, filters: {}},
        # }
        mutation = copy.deepcopy(item)
        if "original" not in mutation:
            mutation["original"] = []

        # Copy/overwrite filters from variables[].filters
        # into top-level filters for current variable mutation.
        try:
            filters = {key: variables[key]["filters"] for key in variables}
        except KeyError:
            filters = {}
        for variable in variables:
            if "filters" in variables[variable]:
                mutation["filters"].update(variables[variable]["filters"])

        # Replace variables in payload and filters
        repvars = {key: variables[key]["value"] for key in variables}
        mutation["payload"] = __replace_variables(mutation["payload"], repvars)
        mutation["filters"].update(__replace_variables(mutation["filters"], repvars))
        mutation["original"].append(item["payload"])

        # Append mutation
        items.append(mutation)

    return items


def __replace_variables(
    data: Union[bool, str, List[str], Dict[str, Any]], variables: Dict[str, str]
) -> Union[bool, str, List[str], Dict[str, Any]]:
    """Replace."""
    temp = copy.deepcopy(data)

    if isinstance(temp, list):
        for i in range(len(temp)):
            temp[i] = __replace_variables(temp[i], variables)
        return temp

    if isinstance(temp, dict):
        for key in temp:
            temp[key] = __replace_variables(temp[key], variables)
        return temp

    if isinstance(temp, str):
        for name, value in variables.items():
            temp = temp.replace(f"{{VAR:{name}}}", value)
        return temp

    return temp
