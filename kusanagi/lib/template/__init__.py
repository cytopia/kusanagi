"""Module that returns template directories."""

from typing import List
import os
import pathlib


TEMPLATE_DIR = "files"


def get_template_dir(dirs: List[str] = []) -> str:
    """Returns absolute path of template dir."""
    path = pathlib.Path(__file__).parent.absolute()
    path = path.parent.absolute()
    path = path.parent.absolute()
    path = os.path.join(path, TEMPLATE_DIR)
    # Add specified sub directories (if any)
    for subdir in dirs:
        path = os.fspath(os.path.join(path, subdir))
    return path
