"""Payload Filter class."""
from typing import Dict, List, Any
from .ds_base_filter import DsBaseFilter


class DsPayloadFilter(DsBaseFilter):
    """Payload Filter Data Structure."""

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
        """Constructor."""
        # Initialize parent class
        super(DsPayloadFilter, self).__init__(
            exe,
            cmd_exe,
            shell,
            cmd_shell,
            sorted(shells),
            sorted(os),
            commands,
            proto,
            direction,
            encoders,
        )
