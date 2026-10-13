"""Gives the keys that the viewer presses."""

from typing import Protocol


class KeySource(Protocol):
    def read_key(self, timeout: float | None) -> str | None: ...
