"""Names for the keys that are not letters."""

from enum import StrEnum


class Key(StrEnum):
    ENTER = "\r"
    ESCAPE = "\x1b"
