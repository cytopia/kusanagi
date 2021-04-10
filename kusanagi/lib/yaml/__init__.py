"""Module to load and validate a yaml configuration file."""

from typing import Dict, Any
from pathlib import PurePath

from .loader import _load
from .validator import _validate_requirements
from .validator import _validate_invalid_keys


def load(path: PurePath, validator: Dict[Any, Any]) -> Dict[Any, Any]:
    """Load yaml file by path and return it as Python dictionary.

    Args:
        path (str): Path to yaml file.
        validator: (Dict[Any, Any]): Yaml dict used to validate a loaded yaml file against.

    Raises:
        OSError: If yaml file cannot not found or read (permission-wise).
        KeyError: If yaml file cannot be parsed or is not valid for its validator.
    """
    data = _load(path)
    try:
        _validate_requirements("", data, validator)  # Ensure all keys are defined
        _validate_invalid_keys("", data, validator)  # Ensure no extra keys are defined
    except KeyError as error:
        raise KeyError(f"{error}\nIn file:{path}") from error
    return data
