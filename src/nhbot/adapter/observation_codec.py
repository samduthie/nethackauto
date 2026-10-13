"""Turns an Observation into JSON data and back, for samples, golden files and replay.

Colors are hex text and glyph rows are numbers in one text line, so that a file stays easy to read.
"""

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from nhbot.adapter.bottom_line import BottomLine
from nhbot.adapter.input_mode import InputMode
from nhbot.adapter.observation import Observation


class ObservationCodec:
    def encode(self, observation: Observation) -> dict[str, Any]:
        return {
            "screen": list(observation.screen),
            "colors": [row.hex() for row in observation.colors],
            "cursor": list(observation.cursor),
            "glyphs": [" ".join(map(str, row)) for row in observation.glyphs],
            "message": observation.message,
            "bottom_line": asdict(observation.bottom_line),
            "input_mode": observation.input_mode.name,
            "game_over": observation.game_over,
        }

    def decode(self, data: Mapping[str, Any]) -> Observation:
        row, column = data["cursor"]
        return Observation(
            screen=tuple(data["screen"]),
            colors=tuple(bytes.fromhex(line) for line in data["colors"]),
            cursor=(row, column),
            glyphs=tuple(tuple(int(glyph) for glyph in line.split()) for line in data["glyphs"]),
            message=data["message"],
            bottom_line=BottomLine(**data["bottom_line"]),
            input_mode=InputMode[data["input_mode"]],
            game_over=data["game_over"],
        )
