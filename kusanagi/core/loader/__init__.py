"""Module to load items from path of files."""

from typing import List, Dict, Any
import sys

from . import yaml
from . import template


def load(files: List[str], subdirs: List[str], validator: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load available payloads from givesn list of files&subdirs and validate them.

    Args:
        files: List of file names.
        subdirs: List of subdirs to traverse into.
        validator: Dictionary to validate yaml against.

    Returns:
        List[dict]: List of loaded and validated items.

    Raises:
        OSError: If yaml file cannot be found or read (permission-wise).
        KeyError: If yaml file cannot be parsed or is not valid for its validator.
    """
    items = []
    paths = []

    for name in files:
        temp = subdirs[:]  # Make a copy of subdirs
        temp.append(name)  # Append name to subdirs
        paths.append(template.get_template_dir(temp))

    for path in paths:
        # Load yaml file and validate
        try:
            data = yaml.load(path, validator)
        except OSError as error:
            print(error.args[0], file=sys.stderr)
            sys.exit(1)
        except KeyError as error:
            print(error.args[0], file=sys.stderr)
            sys.exit(1)

        for item in data["items"]:
            # Append list items
            items.append(item)
    return items
