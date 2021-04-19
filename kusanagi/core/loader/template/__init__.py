"""Module that returns template directories."""

from typing import List
import os
import pathlib


TEMPLATE_DIR = "files"


def get_template_dir(dirs: List[str] = []) -> pathlib.PurePath:
    """Returns absolute path of template dir."""
    path = pathlib.PurePath(__file__)
    path = path.parent
    path = path.parent
    path = path.parent
    path = path.parent
    path = path.joinpath(TEMPLATE_DIR)
    # Add specified sub directories (if any)
    for subdir in dirs:
        path = path.joinpath(subdir)
    return path
