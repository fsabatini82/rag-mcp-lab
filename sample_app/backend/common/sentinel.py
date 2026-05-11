"""Sentinel value for distinguishing 'argument not passed' from 'None'.

See ADR-002 and BUG-502. This is the canonical project pattern — do not
reimplement it locally.
"""

from __future__ import annotations

from typing import Final


class _UnsetType:
    """Singleton type signaling 'argument was not supplied'."""

    _instance: "_UnsetType | None" = None

    def __new__(cls) -> "_UnsetType":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "<UNSET>"

    def __bool__(self) -> bool:
        return False


UNSET: Final = _UnsetType()
