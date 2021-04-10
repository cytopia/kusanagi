"""Payload class."""
from typing import Dict, List, Any
from .ds_payload_filter import DsPayloadFilter


class DsPayload:
    """Payload Data Structure."""

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------
    @property
    def name(self) -> str:
        """Returns name."""
        return self.__name

    @property
    def desc(self) -> str:
        """Returns description."""
        return self.__desc

    @property
    def info(self) -> List[str]:
        """Returns a list of info texts."""
        return self.__info

    @property
    def group(self) -> str:
        """Returns payload group."""
        return self.__group

    @property
    def meta(self) -> Dict[str, Any]:
        """Returns meta information."""
        return self.__meta

    @property
    def filters(self) -> DsPayloadFilter:
        """Returns filters."""
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
        info: List[str],
        group: str,
        meta: Dict[str, Any],
        filters: DsPayloadFilter,
        payload: str,
        original: List[str],
    ) -> None:
        """Constructor."""
        self.__name = name
        self.__desc = desc
        self.__info = info
        self.__group = group
        self.__meta = meta
        self.__filters = filters
        self.__payload = payload
        self.__original = original
