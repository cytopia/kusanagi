"""Payload module."""
from typing import Dict, List, Any
from .ds_payload_filter import DsPayloadFilter


class DsPayload:
    """Data Structure for parsed payload (Cmd, Code or File)."""

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------
    @property
    def name(self) -> str:
        """Returns payload name."""
        return self.__name

    @property
    def desc(self) -> str:
        """Returns payload description."""
        return self.__desc

    @property
    def group(self) -> str:
        """Returns payload group."""
        return self.__group

    @property
    def filters(self) -> DsPayloadFilter:
        """Returns payload filters."""
        return self.__filters

    @property
    def payload(self) -> str:
        """Returns payload string."""
        return self.__payload

    @property
    def original(self) -> List[str]:
        """Returns a list of original payload strings before mutation/compression."""
        return self.__original

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        desc: str,
        group: str,
        filters: DsPayloadFilter,
        payload: str,
        original: List[str],
    ) -> None:
        self.__name = name
        self.__desc = desc
        self.__group = group
        self.__filters = filters
        self.__payload = payload
        self.__original = original
