"""Validate a yaml file."""

from typing import Dict, Any
import re


def _validate_invalid_keys(section: str, data: Dict[str, Any], validator: Dict[str, Any]) -> None:
    for key in data:
        # Check if defined key should not be defined
        if key not in validator:
            raise KeyError(f"[CONFIG-FAIL] {section} invalid key defined: {key}")

        # Recurse into childs
        if validator[key]["childs"]:
            if isinstance(data[key], dict):
                _validate_invalid_keys(section + f"[{key}]", data[key], validator[key]["childs"])
            if isinstance(data[key], list):
                for index, value in enumerate(data[key]):
                    _validate_invalid_keys(
                        section + f"[{key}][{index}]", value, validator[key]["childs"]
                    )


def _validate_requirements(section: str, data: Dict[str, Any], validator: Dict[str, Any]) -> None:
    """Checks if data meets all requirements from validator dict.

    This is a forward validation, where it will be ensured that data contains
    required keys of correct type and correct values.

    Args:
        section (str): Name of the current yaml/dict section.
        data (Dict[Any, Any]): Yaml dict to validate.
        validator (Dict[Any, Any]): Yaml dict used to validate the yaml_dict against.

    Raises:
        KeyError: If data is invalid according to its validator definition.
    """
    for key in validator:

        # Check Required
        if validator[key]["required"] and key not in data:
            raise KeyError(f"[CONFIG-FAIL] {section}[{key}] not defined, but required")

        # Check Type
        if key in data and not isinstance(data[key], validator[key]["type"]):
            req_type = validator[key]["type"]
            has_type = type(data[key])
            raise KeyError(
                f"[CONFIG-FAIL] {section}[{key}] must be of type: {req_type} (is: {has_type})"
            )

        # Check Allowed value by Regex
        if key in data and "allowed" in validator[key]:
            regex = validator[key]["allowed"]
            value = str(data[key])
            if not re.findall(regex, value):
                raise KeyError(f"[CONFIG-FAIL] {section}[{key}] = '{value}' must match: '{regex}'")

        # Recurse into childs
        if key in data and validator[key]["childs"]:
            if isinstance(data[key], dict):
                _validate_requirements(section + f"[{key}]", data[key], validator[key]["childs"])
            if isinstance(data[key], list):
                for index, value in enumerate(data[key]):
                    _validate_requirements(
                        section + f"[{key}][{index}]", data[key][index], validator[key]["childs"]
                    )
