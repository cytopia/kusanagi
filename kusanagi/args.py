"""Parse command line arguments."""

import argparse
import sys

from .defaults import DEF_BIN, DEF_DESC, DEF_VERSION, DEF_AUTHOR, DEF_GITHUB
from .defaults import DEF_PORT
from .core.encoder import argparse_encoder_validate

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
    parser_code.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    parser_file = payload_parser.add_parser(
        "file",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        help="Inject source code in a file (e.g.: php in jpeg).",
        usage="""%(prog)s file [options] addr [port]
       %(prog)s file -h, --help"""
        % ({"prog": DEF_BIN}),
    )
    parser_file.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print(file=sys.stderr)
        print("Error: the following arguments are required: <payload>", file=sys.stderr)
        sys.exit(1)

    # --------------------------------------------------------------------------
    # Command parser: positional
    # --------------------------------------------------------------------------
    cmd_positional = parser_cmd.add_argument_group("positional arguments")
    cmd_positional.add_argument(
        "addr",
        type=str,
        help="""Address to listen or connect to.

""",
    )
    cmd_positional.add_argument(
        "port",
        nargs="?",
        type=int,
        default=DEF_PORT,
        help="""(Optional) Port to listen or connect to
Default: %(port)i

"""
        % ({"port": DEF_PORT}),
    )

    # --------------------------------------------------------------------------
    # Command parser: query arguments
    # --------------------------------------------------------------------------
    cmd_query = parser_cmd.add_argument_group("query arguments")
    cmd_query.add_argument(
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
    cmd_query.add_argument(
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
    cmd_query.add_argument(
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
    cmd_query.add_argument(
        "-o",
        "--os",
        type=str,
        choices=["bsd", "linux", "mac", "windows"],
        default="",
        help="""Only fetch payloads which work on a specific operating system.
Default: fetch for all OS.

""",
    )
    cmd_query.add_argument(
        "-m",
        "--maxlen",
        type=int,
        metavar="bytes",
        default="0",
        help="""Exclude any payloads exceeding the specified max length.

""",
    )

    # --------------------------------------------------------------------------
    # Command parser: mutate arguments
    # --------------------------------------------------------------------------
    cmd_mutate = parser_cmd.add_argument_group("mutate arguments")
    cmd_mutate.add_argument(
        "--enc",
        nargs="+",
        default=[],
        metavar="name",
        type=argparse_encoder_validate,
        help="""Encode shell code with one or more encoders.
When encoding multiple times, pay attention to the
order of specifying encoders.
Note that any filtering (-b, -o, etc) is not done on the
encoded payload. Filtering is done before.
To view available encoders, use --list-encoders.""",
    )

    # --------------------------------------------------------------------------
    # Command parser: helper arguments
    # --------------------------------------------------------------------------
    cmd_helper = parser_cmd.add_argument_group("helper arguments")
    cmd_helper.add_argument(
        "-q",
        "--quick",
        action="store_true",
        help="""Show quick payload results (less detail).

""",
    )
    cmd_helper.add_argument(
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

    # --------------------------------------------------------------------------
    # Command parser: misc arguments
    # --------------------------------------------------------------------------
    cmd_misc = parser_cmd.add_argument_group("misc arguments")
    cmd_misc.add_argument("-h", "--help", action="help", help="Show this help message and exit")

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
    return parser.parse_args()
