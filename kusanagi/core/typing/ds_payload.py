"""Payload class."""
from typing import Dict, List, Any
from .ds_base import DsBase
from .ds_payload_filter import DsPayloadFilter


class DsPayload(DsBase):
    """Payload Data Structure."""

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------
    @property
    def filters(self) -> DsPayloadFilter:
        """Returns filters."""
        return self.__filters

    @property
    def group(self) -> str:
        """Returns payload group."""
        return self.__group

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
        # Initialize parent class
        super(DsPayload, self).__init__(name, desc, info, meta, filters, payload)

        # Initialize variables
        self.__group = group
        self.__filters = filters
        self.__original = original
