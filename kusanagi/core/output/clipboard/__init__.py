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
        # Need to copy to secondary first (due to lazy loading)
        # And then the 'primary=' key is available.
        # https://github.com/asweigart/pyperclip/issues/190
        pyperclip.copy(data)
        pyperclip.copy(data, primary=True)
    except pyperclip.PyperclipException as error:
        raise OSError(error) from error
