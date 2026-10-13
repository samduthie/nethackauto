"""One key press that the bot sends to the game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    key: str
