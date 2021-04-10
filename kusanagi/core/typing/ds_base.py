"""Base class."""
from typing import Dict, List, Any
from .ds_base_filter import DsBaseFilter


class DsBase:
    """Base Data Structure for obsuscators and payloads to inherit from."""

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
    def meta(self) -> Dict[str, Any]:
        """Returns meta information."""
        return self.__meta

    @property
    def filters(self) -> DsBaseFilter:
        """Returns filters."""
        return self.__filters

    @property
    def payload(self) -> str:
        """Returns payload string."""
        return self.__payload

    # --------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        desc: str,
        info: List[str],
        meta: Dict[str, Any],
        filters: DsBaseFilter,
        payload: str,
    ) -> None:
        self.__name = name
        self.__desc = desc
        self.__info = info
        self.__meta = meta
        self.__filters = filters
        self.__payload = payload
