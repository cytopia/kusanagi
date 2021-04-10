"""Module that simply returns the path of this directory to be used when loading available files."""

import os
import pathlib


def get_obfuscator_data_dir() -> str:
    """Returns absolute path of obfuscator data dir."""
    path = os.fspath(pathlib.Path(__file__).parent.absolute())
    path = os.fspath(os.path.join(path, "obfuscators"))
    return path
