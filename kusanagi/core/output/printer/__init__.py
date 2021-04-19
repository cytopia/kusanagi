"""Module to print to terminal with or without colors."""

from typing import Optional, Any
import sys

from termcolor import cprint


class Printer:
    """stdout, stderr print class with color support."""

    def __init__(self, colored: bool) -> None:
        self.__colored = colored

    def stderr(self, text: str, color: Optional[str] = None, **kwargs: Any) -> None:
        """Print to stderr with or without color depending on instance settings."""
        if self.__colored:
            cprint(text, color, file=sys.stderr, **kwargs)
        else:
            print(text, file=sys.stderr, **kwargs)

    def stdout(self, text: str, color: Optional[str] = None, **kwargs: Any) -> None:
        """Print to stdout with or without color depending on instance settings."""
        if self.__colored:
            cprint(text, color, **kwargs)
        else:
            print(text, **kwargs)
