"""Parse command line arguments."""

import argparse
import sys

from .defaults import DEF_BIN, DEF_DESC, DEF_VERSION, DEF_AUTHOR, DEF_GITHUB
from .defaults import DEF_PORT
from .core.output.encoder import argparse_encoder_validate

# from .core.encoder import argparse_encoder_list


# class ListEncoderAction(argparse.Action):
#     """Argument action to list available encoder."""
#
#     def __init__(
#         self,
#         option_strings,
#         dest,
#         const=None,
#         default=None,
#         required=False,
#         help=None,
#         metavar=None,
#     ):
#         super(ListEncoderAction, self).__init__(
#             option_strings=option_strings,
#             dest=dest,
#             nargs=0,
#             const=const,
#             default=default,
#             required=required,
#             help=help,
#         )
#
#     def __call__(self, parser, namespace, values, option_string=None):
#         """Custom action entrypoint."""
#         argparse_encoder_list()
#         sys.exit(0)
#
#    # def __init__(self, option_strings, dest, nargs=None, **kwargs):
#    #     super(ListEncoderAction, self).__init__(option_strings, dest, **kwargs)
#
#    # def __call__(self, parser, namespace, values, option_string=None):
#    #     print('%r %r %r' % (namespace, values, option_string))
#    #     #setattr(namespace, self.dest, values)


def args_addr(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create addr positional argumenmt."""
    argument_group.add_argument(
        "addr",
        type=str,
        help="""Address to listen or connect to.

""",
    )


def args_port(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create port positional argumenmt."""
    argument_group.add_argument(
        "port",
        nargs="?",
        type=int,
        default=DEF_PORT,
        help="""(Optional) Port to listen or connect to
Default: %(port)i

"""
        % ({"port": DEF_PORT}),
    )


def args_lang(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -l/--lang argumenmt."""
    argument_group.add_argument(
        "-l",
        "--lang",
        type=str,
        nargs="+",
        default=[],
        help="""The payload language to query.
(e.g.: perl, python, php, etc)
Default: do not filter language.

""",
    )


def args_exe(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -e/--exe argumenmt."""
    argument_group.add_argument(
        "-e",
        "--exe",
        type=str,
        nargs="+",
        default="",
        help="""Command that will execute the payload
(e.g.: perl, python, php, nc, sh, bash, cmd, PowerShell, etc)
Default: do not filter by underlying command.

""",
    )


def args_shell(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -s/--shell argumenmt."""
    argument_group.add_argument(
        "-s",
        "--shell",
        type=str,
        nargs="+",
        default=[],
        help="""Shell on which the command (specified via -e)
will be executed. Some payloads use crazy output
redirections or pipes that will only work on certain
underlying shells.
(e.g.: dash, sh, bash, zsh, cmd, PowerShell)
Default: do not filter by underlying shell.

""",
    )


def args_badchars(  # pylint: disable=protected-access
    argument_group: argparse._ArgumentGroup,
) -> None:
    """Create -b/--badchars argumenmt."""
    argument_group.add_argument(
        "-b",
        "--badchars",
        type=str,
        default="",
        help="""Exclude any payloads that contain the specified bad chars.
This comes in handy if you encounter a Web Application Firewall
that prohibits certain characters.
Default: Ignore badchars

""",
    )


def args_os(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -o/--os argumenmt."""
    argument_group.add_argument(
        "-o",
        "--os",
        type=str,
        choices=["bsd", "linux", "mac", "solaris", "windows"],
        default="",
        help="""Only fetch payloads which work on a specific operating system.
Default: fetch for all OS.

""",
    )


def args_maxlen(  # pylint: disable=protected-access
    argument_group: argparse._ArgumentGroup,
) -> None:
    """Create -m/--maxlen argumenmt."""
    argument_group.add_argument(
        "-m",
        "--maxlen",
        type=int,
        metavar="bytes",
        default="0",
        help="""Exclude any payloads exceeding the specified max length.

""",
    )


def args_obfuscate(  # pylint: disable=protected-access
    argument_group: argparse._ArgumentGroup,
) -> None:
    """Create --obf argumenmt."""
    argument_group.add_argument(
        "--obf",
        action="store_true",
        help="""Run the fun. This switch will apply obfuscator to all
payloads to get a different set of badchars.

""",
    )


def args_enc(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create --enc argumenmt."""
    argument_group.add_argument(
        "--enc",
        nargs="+",
        default=[],
        metavar="name",
        type=argparse_encoder_validate,
        help="""Encode the output with one or more encoders.
When encoding multiple times, pay attention to the
order of specifying encoders.
Note that any filtering (-b, -o, etc) is not done on the
encoded payload. Filtering is done before.
To view available encoders, use --list-encoders.""",
    )


def args_quick(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -q/--quick argumenmt."""
    argument_group.add_argument(
        "-q",
        "--quick",
        action="store_true",
        help="""Show quick payload results (less detail).

""",
    )


def args_copy(argument_group: argparse._ArgumentGroup) -> None:  # pylint: disable=protected-access
    """Create -c/--copy argumenmt."""
    argument_group.add_argument(
        "-c",
        "--copy",
        nargs="?",
        metavar="index",
        type=int,
        default="-1",
        help="""Copy last shown payload to clipboard or specify index
of payload to copy to clipboard.
(indices are shown in square brackets next to payload)

""",
    )


def _get_version():
    # type: () -> str
    """Return version information."""
    return """%(prog)s: Version %(version)s
(%(url)s) by %(author)s""" % (
        {"prog": DEF_BIN, "version": DEF_VERSION, "url": DEF_GITHUB, "author": DEF_AUTHOR}
    )


def get_args() -> argparse.Namespace:
    """Retrieve command line arguments."""
    # --------------------------------------------------------------------------
    # Main parser
    # --------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        usage="""%(prog)s <payload> [options] addr [host]
       %(prog)s <payload> -h
       %(prog)s -v, --version
       %(prog)s -h, --help"""
        % ({"prog": DEF_BIN}),
        description=DEF_DESC,
    )

    misc = parser.add_argument_group("misc arguments")
    misc.add_argument(
        "-v",
        "--version",
        action="version",
        version=_get_version(),
        help="Show version information and exit",
    )
    misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    # --------------------------------------------------------------------------
    # Payload parser
    # --------------------------------------------------------------------------
    payload_parser = parser.add_subparsers(
        metavar="<payload>",
        dest="payload",
    )
    parser_cmd = payload_parser.add_parser(
        "cmd",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        help="Generate a command to be executed on a shell.",
        usage="""%(prog)s cmd [options] addr [port]
       %(prog)s cmd -h, --help"""
        % ({"prog": DEF_BIN}),
    )
    parser_code = payload_parser.add_parser(
        "code",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        help="Generate source code (e.g.: php).",
        usage="""%(prog)s code [options] addr [port]
       %(prog)s code -h, --help"""
        % ({"prog": DEF_BIN}),
    )

    parser_file = payload_parser.add_parser(
        "file",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        help="Inject source code in a file (e.g.: php in jpeg).",
        usage="""%(prog)s file [options] addr [port]
       %(prog)s file -h, --help"""
        % ({"prog": DEF_BIN}),
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print(file=sys.stderr)
        print("Error: the following arguments are required: <payload>", file=sys.stderr)
        sys.exit(1)

    # --------------------------------------------------------------------------
    # Positional
    # --------------------------------------------------------------------------
    cmd_positional = parser_cmd.add_argument_group("positional arguments")
    code_positional = parser_code.add_argument_group("positional arguments")
    file_positional = parser_file.add_argument_group("positional arguments")

    # positional addr
    args_addr(cmd_positional)
    args_addr(code_positional)
    args_addr(file_positional)

    # positional [port]
    args_port(cmd_positional)
    args_port(code_positional)
    args_port(file_positional)

    # --------------------------------------------------------------------------
    # Query arguments
    # --------------------------------------------------------------------------
    cmd_query = parser_cmd.add_argument_group("query arguments")
    code_query = parser_code.add_argument_group("query arguments")
    file_query = parser_file.add_argument_group("query arguments")

    # -l/--lang
    args_lang(code_query)

    # -e/--exe
    args_exe(cmd_query)
    args_exe(file_query)

    # -s/--shell
    args_shell(cmd_query)
    args_shell(code_query)
    args_shell(file_query)

    # -b/--badchars
    args_badchars(cmd_query)
    args_badchars(code_query)
    args_badchars(file_query)

    # -o/--os
    args_os(cmd_query)
    args_os(code_query)
    args_os(file_query)

    # -m/--maxlen
    args_maxlen(cmd_query)
    args_maxlen(code_query)
    args_maxlen(file_query)

    # --------------------------------------------------------------------------
    # Mutate arguments
    # --------------------------------------------------------------------------
    cmd_mutate = parser_cmd.add_argument_group("mutate arguments")
    code_mutate = parser_code.add_argument_group("mutate arguments")
    file_mutate = parser_file.add_argument_group("mutate arguments")

    # --obf
    args_obfuscate(code_mutate)
    args_obfuscate(cmd_mutate)

    # --enc
    args_enc(cmd_mutate)
    args_enc(code_mutate)
    args_enc(file_mutate)

    # --------------------------------------------------------------------------
    # Helper arguments
    # --------------------------------------------------------------------------
    cmd_helper = parser_cmd.add_argument_group("helper arguments")
    code_helper = parser_code.add_argument_group("helper arguments")
    file_helper = parser_file.add_argument_group("helper arguments")

    # -q/--quick
    args_quick(cmd_helper)
    args_quick(code_helper)
    args_quick(file_helper)

    # -c/--copy
    args_copy(cmd_helper)
    args_copy(code_helper)
    args_copy(file_helper)

    # --------------------------------------------------------------------------
    # Misc arguments
    # --------------------------------------------------------------------------
    cmd_misc = parser_cmd.add_argument_group("misc arguments")
    code_misc = parser_code.add_argument_group("misc arguments")
    file_misc = parser_file.add_argument_group("misc arguments")

    # -h/--help
    cmd_misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    code_misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    file_misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    #
    # TODO:
    # TODO: -o/--obfuscate   Run the Fun!

    # TODO:
    # TODO: -n/--noob   Turn on noob mode
    #
    #
    # -q [no] o <OS>, [<OS>]
    # -q p/proto <PROTO>
    # -q d/dir   <DIRECTION>
    # -q e/exe   <EXECUTABLE>
    # -q s/shell <SHELL>
    # -q c/cmd   <COMMANDS>
    # -q b/bad   <BADCHARS>

    # -o/--obfuscate
    # -e/--encode
    # -n/--noob

    #  -c/--copy [num] (by default last one)
    # mutate = parser.add_argument_group("mutate arguments")
    # mutate.add_argument("-e", "--encode", help="Encode")

    # positional = parser.add_argument_group("positional arguments")
    # query = parser.add_argument_group("query arguments")
    # mutate = parser.add_argument_group("mutate arguments")
    # listing = parser.add_argument_group("listing arguments")
    # optional = parser.add_argument_group("optional arguments")

    # --------------------------------------------------------------------------
    # Positional arguments
    # --------------------------------------------------------------------------
    #    positional.add_argument(
    #        "payload",
    #        type=str,
    #        choices=["cmd", "code"],
    #        help="""Payload to generate.
    # cmd:  generate a command to be executed on a shell.
    # code: generate executable code (e.g.: php)
    #
    # """
    #     )
    #     positional.add_argument(
    #         "addr",
    #         nargs="?",
    #         type=str,
    #         help="""(Optional) Address to listen or connect to
    #
    # """
    #     )
    #     positional.add_argument(
    #         "port",
    #         nargs="?",
    #         type=int,
    #         default=DEF_PORT,
    #         help="""(Optional) Port to listen or connect to
    # Default: %(port)i
    #
    # """
    #         % ({"port": DEF_PORT}),
    #     )

    #     cmd_test_arg = parser_cmd.add_argument_group("test group")
    #     cmd_test_arg.add_argument(
    #         "port",
    #         nargs="?",
    #         type=int,
    #         default=DEF_PORT,
    #         help="""(Optional) Port to listen or connect to
    # Default: %(port)i
    # """
    #         % ({"port": DEF_PORT}),
    #     )
    # cmd_test_arg.add_argument(
    #  "-h", "--help", action="help", help="Show this help message and exit")

    # --------------------------------------------------------------------------
    # Query arguments
    # --------------------------------------------------------------------------

    #    # -q/--query 1
    #    # -q/--query os linux
    #    # -q/--query os mac
    #    # -q/--query shell bind
    #    # -q/--query proto tcp
    #    # -b/--badchars "'"
    #    # -l/--lang
    #    query.add_argument(
    #        "-q",
    #        "--query",
    #        nargs="+",
    #        default=[],
    #        action='append',
    #        help="""Query shells based on conditions.
    # """
    #    )
    #
    #
    #    # --------------------------------------------------------------------------
    #    # Mutate arguments
    #    # --------------------------------------------------------------------------
    #    mutate.add_argument(
    #        "-e",
    #        "--encode",
    #        nargs="+",
    #        default=[],
    #        metavar="name",
    #        type=argparse_encoder_validate,
    #        help="""Encode shell code with one or more encoders.
    # When encoding multiple times, pay attention to the
    # order of specifying encoders.
    # To view available encoders, use --list-encoders."""
    #    )
    #    mutate.add_argument(
    #        "--quote",
    #        choices=["single", "double", "auto"],
    #        default="auto",
    #        type=str,
    #        help="""Set the quoting style for inner and outer quotes.
    # Some quotes are fixed (not changeable), depending on the
    # programming language, operating system or the way it is
    # handed over to a command.
    # By default, this option is set to auto, which uses
    # single quotes on the outside and double quotes inside."""
    #    )
    #
    #    # -q/--quote single, double, auto
    #    # -s/--shell sh, /bin/sh, bash, auto
    #    # -w/--wrapper cmd, gif, jpg, none
    #    # -e/--encode base64 url
    #    # -q/--query 1
    #    # -q/--query os linux
    #    # -q/--query os mac
    #    # -q/--query shell bind
    #    # -q/--query proto tcp
    #    # -b/--badchars "'"
    #    # -l/--lang
    #
    #    listing.add_argument(
    #        "--list-languages",
    #        action='store_true',
    #        help="""List available languages"""
    #    )
    #    listing.add_argument(
    #        "--list-payloads",
    #        action='store_true',
    #        help="""List available payloads"""
    #    )
    #    listing.add_argument(
    #        "--list-wrapper",
    #        action='store_true',
    #        help="""List available payloads wrapper"""
    #    )
    #    listing.add_argument(
    #        "--list-encoders",
    #        action=ListEncoderAction,
    #        help="""List available encoder"""
    #    )
    #
    # Return arguments
    parsed = parser.parse_args()
    return parsed
