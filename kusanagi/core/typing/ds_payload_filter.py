"""Payload Filter class."""
from typing import List


class DsPayloadFilter:
    """Payload Filter Data Structure."""

    @property
    def exe(self) -> str:
        """Returns the executable to run the payload."""
        return self.__exe

    @property
    def shell(self) -> str:
        """Returns a list of underlying shells on which the payload works."""
        return self.__shell

    @property
    def cmd_exe(self) -> str:
        """Returns the executable to run the payload."""
        return self.__cmd_exe

    @property
    def cmd_shell(self) -> str:
        """Returns a list of underlying shells on which the payload works."""
        return self.__cmd_shell

    @property
    def shells(self) -> List[str]:
        """Returns a list of underlying shells on which the payload works."""
        return self.__shells

    @property
    def os(self) -> List[str]:
        """Returns a list of operating systems on which the payload works."""
        return self.__os

    @property
    def commands(self) -> List[str]:
        """Returns a list of additional commands used by the payload."""
        return self.__commands

    @property
    def proto(self) -> str:
        """Returns the protocol used by the payload: 'tcp' or 'udp'."""
        return self.__proto

    @property
    def direction(self) -> str:
        """Returns the payload shell type: 'bind' or 'reverse'."""
        return self.__direction

    @property
    def encoders(self) -> List[str]:
        """Returns list of used encoder functions."""
        return self.__encoders

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(
        self,
        exe: str,
        cmd_exe: str,
        shell: str,
        cmd_shell: str,
        shells: List[str],
        os: List[str],
        commands: List[str],
        proto: str,
        direction: str,
        encoders: List[str],
    ) -> None:
        self.__exe = exe
        self.__shell = shell
        self.__cmd_exe = cmd_exe
        self.__cmd_shell = cmd_shell
        self.__shells = sorted(shells)
        self.__os = sorted(os)
        self.__commands = commands
        self.__proto = proto
        self.__direction = direction
        self.__encoders = encoders
