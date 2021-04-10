"""Clipboard module."""

import pyperclip  # type: ignore

# IMPORTANT:
# On Windows, no additional modules are needed.
#
# On Mac, this module makes use of the pbcopy and pbpaste commands, which should come with the os.
#
# On Linux, this module makes use of the xclip or xsel commands, which should come with the os.
# Otherwise run “sudo apt-get install xclip” or “sudo apt-get install xsel”
# (Note: xsel does not always seem to work.)
#
# Otherwise on Linux, you will need the gtk or PyQt4 modules installed.


def copy_to_clipboard(data: str) -> None:
    """Copy text to clipboard.

    Raises:
        OSError if clipboard fails.
    """
    try:
        pyperclip.copy(data)
    except pyperclip.PyperclipException as error:
        raise OSError(error) from error
