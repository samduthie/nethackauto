"""Writes each event as one line of JSON, with the game id first.

Input: events. Output: lines on a text stream.
"""

import json
from typing import TextIO

from nhbot.telemetry.event import Event


class JsonLinesWriter:
    def __init__(self, stream: TextIO, game_id: str) -> None:
        self._stream = stream
        self._game_id = game_id

    def write(self, event: Event) -> None:
        self._stream.write(json.dumps({"game": self._game_id, **event.to_dict()}) + "\n")
