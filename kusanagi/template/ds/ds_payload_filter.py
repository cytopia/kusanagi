"""Payload module."""
from typing import Dict, List, Any


class DsPayloadFilter:
    """Data Structure for Payload filters."""

    @property
    def exe(self) -> str:
        """Returns the executable to run the payload."""
        return self.__exe

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
    def obfuscator(self) -> List[str]:
        """Returns list of used obfuscator functions."""
        return self.__obfuscator

    def __init__(
        self,
        exe: str,
        shells: List[str],
        os: List[str],
        commands: List[str],
        proto: str,
        direction: str,
        obfuscator: List[str],
    ) -> None:
        self.__exe = exe
        self.__shells = shells
        self.__os = os
        self.__commands = commands
        self.__proto = proto
        self.__direction = direction
        self.__obfuscator = obfuscator
