"""Load a yaml file."""

from typing import Dict, Any

import errno
import os
import yaml


def _load(path: str) -> Dict[Any, Any]:
    """Load yaml file by path and return it as Python dictionary.

    Args:
        path (str): Path to yaml file.

    Returns:
        dict: Python dict from yaml file.

    Raises:
        OSError: If file not found or yaml cannot be read.
        KeyError: If file cannot be parsed.
    """
    try:
        file_p = open(path)
    except FileNotFoundError as err_file:
        error = os.strerror(errno.ENOENT)
        raise OSError(f"[ERROR] File does not exist: {path}\n{error}")
    except PermissionError as err_perm:
        error = os.strerror(errno.EACCES)
        raise OSError(f"[ERROR] No permission to load file form: {path}\n{error}")
    else:
        try:
            return dict(yaml.safe_load(file_p))
        except yaml.YAMLError as err_yaml:
            error = str(err_yaml)
            raise KeyError(f"[ERROR]: {path}\n{error}") from err_yaml
        finally:
            file_p.close()
