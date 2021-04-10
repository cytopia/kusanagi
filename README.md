# kusanagi

**TL;DR:** `kusanagi` is a bind- and reverse shell payload generator.


[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/kusanagi)](https://pypi.org/project/kusanagi/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kusanagi)](https://pypi.org/project/kusanagi/)
[![PyPI - Format](https://img.shields.io/pypi/format/kusanagi)](https://pypi.org/project/kusanagi/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/kusanagi)](https://pypi.org/project/kusanagi/)
[![PyPI - License](https://img.shields.io/pypi/l/kusanagi)](https://pypi.org/project/kusanagi/)


[![Build Status](https://github.com/cytopia/kusanagi/workflows/linting/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=linting)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/building/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=building)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/testing/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=testing)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/black/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=black)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/mypy/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=mypy)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/pylint/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=pylint)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/pycode/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=pycode)
[![Build Status](https://github.com/cytopia/kusanagi/workflows/pydoc/badge.svg)](https://github.com/cytopia/kusanagi/actions?workflow=pydoc)


At its core, it is just a collection of Yaml files that define various *shell commands*,
*code snippets*, *file specifications* and *obfuscators*. It combines and permutates all of them to generate
payloads according to someone's need.

**Payloads** are highly searchable and filterable in order
to generate a *code-*, *file-* or *command* injection with correct binaries for the target architecture
and removed bad chars that might get filtered/denied by certain mechanisms which are in between you and the target (e.g.: web application firewall).

**Disclaimer:** It does have a *copy-to-clipboard* function to eliminate heavy mouse gestures.

<img src="doc/screenshot01.png" height="300px;" style="height: 300px;" />



## Current state

`kusanagi` is currently at most an alpha version and in a very early state of development.

Feel free to use it, but expect drastic changes in ui and available command line arguments.

If you want to support this project, drop me all your payloads and obfuscators you know about.



## Install
```bash
pip install kusanagi
```


## Requirements

* Python >= 3.6
* [requirements.txt](requirements.txt)



## Usage

#### General
```bash
usage: kusa <payload> [options] addr [host]
       kusa <payload> -h
       kusa -v, --version
       kusa -h, --help

Kusanagi is a bind and reverse shell payload generator with obfuscation and badchar support.

positional arguments:
  <payload>
    cmd          Generate a command to be executed on a shell.
    code         Generate source code (e.g.: php).
    file         Inject source code in a file (e.g.: php in jpeg).

misc arguments:
  -v, --version  Show version information and exit
  -h, --help     Show this help message and exit
```

#### cmd
```bash
usage: kusa cmd [options] addr [port]
       kusa cmd -h, --help

positional arguments:
  addr                  Address to listen or connect to.

  port                  (Optional) Port to listen or connect to
                        Default: 4444


query arguments:
  -e EXE [EXE ...], --exe EXE [EXE ...]
                        Command that will execute the payload
                        (e.g.: perl, python, php, nc, sh, bash, cmd, PowerShell, etc)
                        Default: do not filter by underlying command.

  -s SHELL [SHELL ...], --shell SHELL [SHELL ...]
                        Shell on which the command (specified via -e)
                        will be executed. Some payloads use crazy output
                        redirections or pipes that will only work on certain
                        underlying shells.
                        (e.g.: dash, sh, bash, zsh, cmd, PowerShell)
                        Default: do not filter by underlying shell.

  -b BADCHARS, --badchars BADCHARS
                        Exclude any payloads that contain the specified bad chars.
                        This comes in handy if you encounter a Web Application Firewall
                        that prohibits certain characters.
                        Default: Ignore badchars

  -o {bsd,linux,mac,windows}, --os {bsd,linux,mac,windows}
                        Only fetch payloads which work on a specific operating system.
                        Default: fetch for all OS.

  -m bytes, --maxlen bytes
                        Exclude any payloads exceeding the specified max length.


mutate arguments:
  --enc name [name ...]
                        Encode shell code with one or more encoders.
                        When encoding multiple times, pay attention to the
                        order of specifying encoders.
                        Note that any filtering (-b, -o, etc) is not done on the
                        encoded payload. Filtering is done before.
                        To view available encoders, use --list-encoders.

helper arguments:
  -q, --quick           Show quick payload results (less detail).

  -c [index], --copy [index]
                        Copy last shown payload to clipboard or specify index
                        of payload to copy to clipboard.
                        (indices are shown in square brackets next to payload)


misc arguments:
  -h, --help            Show this help message and exit
```


## License

**[MIT License](LICENSE.txt)**

Copyright (c) 2021 **[cytopia](https://github.com/cytopia)**
